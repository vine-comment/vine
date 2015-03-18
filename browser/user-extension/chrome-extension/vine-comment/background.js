chrome.browserAction.onClicked.addListener(function(tab) {
    console.log("x1")
    chrome.tabs.captureVisibleTab(null, function(img) {
        console.log("x2")
        var xhr = new XMLHttpRequest(), formData = new FormData();  
        formData.append("img", img);
        xhr.open("POST", "http://www.tengmanpinglun.com/document/upload", true);
        xhr.send(formData);
    });
});
