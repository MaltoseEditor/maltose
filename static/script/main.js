function compare(obj_1, obj_2) {
    var _1 = obj_1["date"];
    var _2 = obj_2["date"];
    if (_2 == _1) {
        _1 = obj_1["update"];
        _2 = obj_2["update"];
        if (_2 == _1) {
            _1 = obj_1["title"]
            _2 = obj_2["title"]
        }
    }
    if (_1 == _2)
        return 0;
    return _1 > _2 ? -1 : 1;
}

$(window).ready(function () {
    GET();
});

$("section").click(function () {
    if ($(window).width() < 567) {
        $("nav").fadeToggle();
        $("aside").fadeToggle();
        $("footer").fadeToggle();
    }
});
