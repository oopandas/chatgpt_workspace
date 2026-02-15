console.log("ChatGPT Logs Extension Loaded!");

setTimeout(() => {
    const userMessages = document.querySelectorAll(
        '[data-message-author-role="user"] .whitespace-pre-wrap'
    );

    if (userMessages.length > 0) {
        userMessages.forEach(msg => {
            console.log(msg.innerText);
        });
    } else {
        console.log("要素が見つかりません");
    }
}, 3000);