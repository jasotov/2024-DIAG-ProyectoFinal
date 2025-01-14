function onLoad() {
    messageInput = document.getElementById('message');
    submitButton = document.getElementById('send-message');

    messageInput.addEventListener('input', (event) => {
        if (event.target.value.length > 0) {
            submitButton.classList.remove('disabled');
        } else {
            submitButton.classList.add('disabled');
        }
    })
}

document.addEventListener('DOMContentLoaded', onLoad);

function addMessageToChat(message) {
    messageHTML = '';

    if (message.author === 'assistant') {
        messageHTML = `
            <div class="d-flex flex-row justify-content-start mb-4">
                <img class="bg-white rounded-circle" src="/static/images/avatar_verflix_3.png" title="verflix" style="width: 45px; height: 45px;">&nbsp;&nbsp;&nbsp;&nbsp;
                <div>
                    <div class="spinner-grow text-info" style="width: 5px; height: 5px;" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-info" style="width: 5px; height: 5px;" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow text-info" style="width: 5px; height: 5px;" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>
            </div>
        `;
    } else {
        messageHTML = `
            <div class="d-flex flex-row justify-content-end mb-4">
                <div>
                    <div class="p-3 me-3 border bg-body-tertiary" style="border-radius: 15px;">
                        <p class="small mb-0">${message.content}</p>
                    </div>
                    <div>
                        <p class="small ms-3 mb-3 rounded-3 text-muted" style="font-size: x-small; text-align: right;">${getCurrentTime()}</p>
                    </div>
                </div>
            </div>
        `;
    }

    document.getElementById('messages').insertAdjacentHTML('beforeend', messageHTML);
}

function submitFreeMessage() {
    const form = document.getElementById("formchat2");
    const formData = new FormData(form);

    submitButton.classList.add('disabled');
    messageInput.classList.add('disabled');
    document.getElementById("text").style.display = 'none';
    document.getElementById("spinner").style.display = 'block';

    addMessageToChat({
        content: formData.get('message'),
        author: 'user',
    });


    addMessageToChat({
        content: '',
        author: 'assistant',
    });

    scrollToBottom("ScrollableDiv");

    form.submit();

    //messageInput.value = '';
}

function getCurrentTime() {
    let CurrentTime = '';

    let d = new Date().toLocaleString("en-US", {timeZone: "America/Santiago"});
    let now = new Date(d)
    let hour = now.getHours();
    let minute = now.getMinutes();

    if (hour < 10) {
        CurrentTime = '0';
    }
    CurrentTime += hour +':';
    if (minute < 10) {
        CurrentTime += '0';
    }
    CurrentTime += minute;

    return CurrentTime;
}
/*
    document.addEventListener('submit', async (event) => {
        event.preventDefault();


        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
               'Accept': 'application/json',
            },
            body: formData
        });

        const message = await response.json();
        addMessageToChat(message);

        messageInput.classList.remove('disabled');
        document.getElementById("text").style.display = 'block';
        document.getElementById("spinner").style.display = 'none';

    })
*/