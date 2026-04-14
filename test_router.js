const url = new URL("http://example.com/stage2");
let serveContent = "stage1";
const data = {
    isMultiStage: true,
    content: "stage1",
    contentStage2: "stage2"
};

if (data.isMultiStage && url.pathname === '/stage2') {
    serveContent = data.contentStage2;
} else if (url.pathname !== '/') {
    serveContent = data.content;
}

console.log(serveContent);
