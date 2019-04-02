function showMenu() {
    if (window.innerWidth < 567) {
        document.getElementsByTagName("nav")[0].classList.toggle("display");
        document.getElementsByTagName("aside")[0].classList.toggle("display");
        document.getElementsByTagName("aside")[1].classList.toggle("display");
        document.getElementsByTagName("aside")[2].classList.toggle("display");
        document.getElementsByTagName("footer")[0].classList.toggle("display");
    }
}

function displayItems(event) {
    var element = event.target;
    while (!element.classList.contains("head")) {
        element = element.parentElement;
    }
    var items = element.nextSibling.nextSibling,
        more = element.getElementsByClassName("more")[0];
    if (items.hidden) {
        items.hidden = false;
        more.classList.add("active");
    } else {
        items.hidden = true;
        more.classList.remove("active");
    }
}

function search_focus(event) {
    event.target.placeholder = "";
}

function search_blur(event) {
    event.target.value = "";
    event.target.placeholder = "搜索";
}

function search_submit(event) {
    if (event.keyCode === 13) {
        window.location.href = "https://www.google.com/search?q=site%3Aabersheeran.com%2Farticles%2F+" + event.target.value.split(" ").join("+");
    }
}

// header跟随
// 已去除, 但代码还可以, 留着以后可以用
// var setHeaderSticky = function () {
//     var header = document.getElementsByTagName("header")[0];
//     var low = true;
//     var headerViewTop = header.offsetTop;
//     var scrollTop = document.body.scrollTop + document.documentElement.scrollTop;
//     var headerViewBottom = scrollTop + window.innerHeight - (header.offsetTop + header.offsetHeight);
//     return function inner() {
//         var documentOffsetHeight = document.body.offsetHeight + document.documentElement.offsetHeight;
//         headerViewTop = header.offsetTop;
//         low = document.body.scrollTop + document.documentElement.scrollTop > scrollTop;
//         scrollTop = document.body.scrollTop + document.documentElement.scrollTop;
//         headerViewBottom = scrollTop + window.innerHeight - (header.offsetTop + header.offsetHeight);
//         if (window.innerWidth > 568 && documentOffsetHeight > scrollTop + window.innerHeight) { // 如果滚动条滚动距离尚未到底
//             if (window.innerHeight - header.offsetHeight < 0) { // 如果header高度高于窗口
//                 if (low) { // 如果是往下滚
//                     if (headerViewBottom > 0) {
//                         header.setAttribute("style", `top: ${header.offsetTop + headerViewBottom}px;`);
//                     }
//                 } else { // 如果是往上滚
//                     if (headerViewTop > scrollTop) {
//                         header.setAttribute("style", `top: ${scrollTop}px;`);
//                     }
//                 }
//             } else { // header高度不高于窗口
//                 header.setAttribute("style", `top: ${scrollTop}px;`);
//             }
//         }
//     }
// }();

// window.addEventListener("scroll", setHeaderSticky);
// window.addEventListener("resize", setHeaderSticky);
