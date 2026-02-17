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

fetch("http://127.0.0.1:8000", {
    method: "POST",//django側の上のurls.pyのリンクにPOSTリクエストを送る
    headers: {
        "Content-Type": "aplication/json"//JSON形式という説明
    },
    body: JSON.stringify()//文字列に変換
})