'use strict'

document.addEventListener('DOMContentLoaded', () => {
    
    const GUID = document.querySelector("#ws-id").value
    const MAIN_URL = `${document.location.host}`;
    
    const message_sender = document.querySelector("#message-sender")
    const send_btn = document.querySelector("#msg-send-btn")
    const flood_btn = document.querySelector("#flood-btn")
    const test_btn = document.querySelector("#test-btn")
    const connect_btn = document.querySelector("#connect-btn")
    const disconnect_btn = document.querySelector("#disconnect-btn")
    
    if (getCookie('session_guid') == undefined){
        setCookie('session_guid', GUID)
    }
    console.log(getCookie('session_guid'))

    let isNewMessage = false
    let isWindowFocused = true

    function WebSocketConnection(hosturl, wsguid){

        let wsconn = new WebSocket(`ws://${hosturl}/ws/${wsguid}`)

        wsconn.onopen = function(event) {
            disconnect_btn.disabled = false
            flood_btn.disabled = false
            send_btn.disabled = false
            connect_btn.disabled = true
            message_sender.addEventListener('submit', sendMessage)
        }

        wsconn.onmessage = function(event) {
            ///console.log(event)
            showMessage(event.data)
        }

        wsconn.onclose = function(event) {
            ///console.log(event)
            if (event.wasClean) {
                showError(`Connection was closed (code ${event.code} ${event.reason? event.reason : ''})`);
            }else{
                showError('Connection interrupted');
            }
            disconnect_btn.disabled = true
            flood_btn.disabled = true
            send_btn.disabled = true
            connect_btn.disabled = false
            message_sender.removeEventListener('submit', sendMessage)
        }

        wsconn.onerror = function(error) {
            showError(error);
            disconnect_btn.disabled = true
            flood_btn.disabled = true
            send_btn.disabled = true
            connect_btn.disabled = false
            message_sender.removeEventListener('submit', sendMessage)
        }

        return wsconn
    }

    function showError(e){
        let error = (typeof e === 'string' || typeof e === 'number')? e : (e.message)? e.message : null
        if (error !== null) {
            let messages = document.getElementById('messages')
            let message = document.createElement('div')
            let content = document.createTextNode(error)
            message.appendChild(content)
            message.classList.add("red")
            messages.appendChild(message)
            if (!isWindowFocused) { isNewMessage = true }
        }
    }
    
    function showMessage(data){
        try{
            let messages = document.getElementById('messages')
            let message = document.createElement('div')
            let msg = JSON.parse(data)
            let content = document.createTextNode(`${msg.time}: ${msg.name? msg.name : msg.guid? msg.guid : ''} - ${msg.msg}`)
            let color = 'black'
            if (msg.msgtype){
                switch(msg.msgtype){
                    case 'status':
                       color = (msg.guid == GUID)? 'purple' : 'maroon'
                       break
                    case 'flood':
                        color = 'gray'
                        break
                    default:
                        color = (msg.guid == GUID)? 'green': 'blue'
                }
            }
            message.appendChild(content)
            message.classList.add(color)
            messages.appendChild(message)
            if (!isWindowFocused) { isNewMessage = true }
        }catch(e){
            showError(e)
        }
    }

    const sendMessage = (event) => {
        let input = document.getElementById("messageText")
        ws.send(input.value)
        input.value = ''
        beep(480, 50)
        event.preventDefault()
    }

    var ws = WebSocketConnection(MAIN_URL, GUID)

    const disconnect = () => {
        ws.close()
        beep(240, 50)
        showError("Disconnected by user")
    }
    disconnect_btn.addEventListener('click', disconnect)

    const connect = () => {
        ws = WebSocketConnection(MAIN_URL, GUID)
        beep(340, 50)
    }
    connect_btn.addEventListener('click', connect)

    async function flood(){
        await fetch(`http://${MAIN_URL}/qq`, {})
        .then(res => {
            beep(520, 50)
        })
        .catch(error => {
            beep(240, 50)
            console.log(error)
            showError(error)
        })
    }
    flood_btn.addEventListener('click', flood)

    /// Автопрокрутка сообщений в конец списка полученных сообщений
    let timer
    let isPaused = false

    window.addEventListener('wheel', function(){
        isPaused = true
        clearTimeout(timer)
        timer = window.setTimeout(function(){
            isPaused = false;
        }, 1000);  
    })
 
    window.setInterval(function(){          
        if(!isPaused){
            window.scrollTo(0, document.body.scrollHeight)
        }
    }, 500)

    /// Мигание заголовка вкладки при получении нового сообщения
    const defaultTitle = document.title

    var changeTitle = function(){
        this.title = function () {
            let title = document.title
            if (isNewMessage){
                document.title = (title == defaultTitle ? "New Message" : defaultTitle)
            }else{
                document.title = defaultTitle
            }
        }
    }

    changeTitle.prototype.start = function() {
        this.timer = setInterval(this.title, 1000)
    }

    changeTitle.prototype.stop = function() {
        clearInterval(this.timer)
    }

    var timerTitle = new changeTitle()
    
    window.onblur = function() {
        isWindowFocused = false
        timerTitle.start()
    }

    window.onfocus = function() {
        isWindowFocused = true
        isNewMessage = false
        document.title = defaultTitle
        timerTitle.stop()
    }

})

function beep(frequency, duracity){
    // создаем аудио контекст
    let audioCtx = new(window.AudioContext || window.webkitAudioContext)();
    // создаем OscillatorNode - генератор
    let oscillator = audioCtx.createOscillator();
    oscillator.type = 'square';
    // задаем частоту в герцах
    oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);
    oscillator.connect(audioCtx.destination);
    // запускаем пищалку
    oscillator.start();
    // говорим "горшочек не вари" через N мс
    setTimeout(e => oscillator.stop(), duracity);
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {
    options = {
        path: '/',
        samesite: 'strict',
    };
    
    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }
    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
    
    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }
    document.cookie = updatedCookie;
}

function removeCookie(name) {
  document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
