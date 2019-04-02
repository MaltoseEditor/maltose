/* 加载博客内容 */

/* 顺序异步加载内容 */
function GET(pre_url = null) {
    if (pre_url == null) {
        var url = next_url();
    }
    else {
        var url = pre_url;
    }
    if (url == null) {
        var load_error = document.getElementById("load_error");
        load_error.hidden = false;
        load_error.innerText = '<end></end>'; // 结束
        document.getElementById("loading").hidden = true;
    }
    else {
        $.ajax({
            type: "GET",
            url: url,
            async: true,
            success: function (datas) {
                for (var i = 0; i < datas.length; i++) {
                    main.blogs.push(datas[i]);
                }
                GET();
            },
            error: function () {
                GET(url)
            }
        });
    }
}

/* 乱序异步加载内容 */
// function GET() {
//     var count = 0;
//     function get_more_blog(url) {
//         $.ajax({
//             type: "GET",
//             url: url,
//             async: true,
//             success: function (datas) {
//                 for (var i = 0; i < datas.length; i++) {
//                     main.blogs.push(datas[i]);
//                 }
//                 count -= 1;
//             },
//             error: function () {
//                 get_more_blog(url);
//             }
//         });
//     }
//     var url = null;
//     $("#loading").fadeIn(1);
//     do {
//         url = next_url();
//         if (url != null) {
//             get_more_blog(url);
//             count += 1;
//         }
//     } while (url != null);

//     function check() {
//         setTimeout(function () {
//             if (count == 0) {
//                 $("#load_error").fadeIn(1);
//                 $("#load_error").text('<end></end>'); // 结束
//                 $("#loading").fadeOut(500);
//                 main.blogs.sort(compare);
//             }
//             else {
//                 check();
//             }
//         });
//     }
//     check();
// }

var next_url = function () {
    var url_list, i = 0, url = null;
    function innerFunc() {
        if (url == null) {
            $.ajax({
                type: "GET",
                url: "/time/index.json",
                async: false,
                success: function (datas) {
                    url_list = datas.reverse();
                },
                error: function () {
                    alert("您的网络似乎有点问题，请检查网络后刷新页面~");
                }
            });
            url = url_list[i]["link"] + "index.json";
            i++;
            return url;
        }
        else if (i < url_list.length) {
            url = url_list[i]["link"] + "index.json";
            i++;
            return url;
        }
        else {
            return null;
        }
    }
    return innerFunc;
}();

(function () { //控制加入的JS
    var d = document,
        s = d.createElement('script');
    s.src = "/STATIC/script/main.js";
    d.head.appendChild(s);
})();
