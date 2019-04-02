var initTop = null,
    stickyElement = null;

function getElementViewTop(element, absolute = false) {
    var actualTop = element.offsetTop;
    var current = element.offsetParent;
    while (current !== null) {
        actualTop += current.offsetTop;
        current = current.offsetParent;
    }
    if (absolute) {
        return actualTop;
    }
    return actualTop - (document.body.scrollTop + document.documentElement.scrollTop);
}

function stickyFunction() {
    var elementViewTop = getElementViewTop(stickyElement),
        scrollTop = document.body.scrollTop + document.documentElement.scrollTop;
    if (elementViewTop < 0) {
        stickyElement.classList.add("sticky");
    }
    if (initTop >= scrollTop) {
        stickyElement.classList.remove("sticky");
    }
}

function remSticky() {
    if (stickyElement != null) {
        stickyElement.classList.remove("sticky");
    }
    stickyElement = null;
    initTop = null;
    window.removeEventListener("scroll", stickyFunction);
    window.removeEventListener("resize", stickyFunction);
}

function setSticky(element) {
    stickyElement = element;
    initTop = getElementViewTop(window.stickyElement, true);
    window.addEventListener("scroll", stickyFunction);
    window.addEventListener("resize", stickyFunction);
}
