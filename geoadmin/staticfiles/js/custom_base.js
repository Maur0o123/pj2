ylp4 = document.all;
ka20 = ylp4 && !document.getElementById;
thji = ylp4 && document.getElementById;
oocf = !ylp4 && document.getElementById;
lbe8 = document.layers;
function ddd8(ahm7) {
try {
    if (ka20) alert("");
} catch (e) {}
if (ahm7 && ahm7.stopPropagation) ahm7.stopPropagation();
return false;
}
function rdn2() {
if (event.button == 2 || event.button == 3) ddd8();
}
function iyic(e) {
return e.which == 3 ? ddd8() : true;
}
function tapq(o4wk) {
for (m8ha = 0; m8ha < o4wk.images.length; m8ha++) {
    o4wk.images[m8ha].onmousedown = iyic;
}
for (m8ha = 0; m8ha < o4wk.layers.length; m8ha++) {
    tapq(o4wk.layers[m8ha].document);
}
}
function i8z9() {
if (ka20) {
    for (m8ha = 0; m8ha < document.images.length; m8ha++) {
    document.images[m8ha].onmousedown = rdn2;
    }
} else if (lbe8) {
    tapq(document);
}
}
function tmvb(e) {
if (
    (thji &&
    event &&
    event.srcElement &&
    event.srcElement.tagName == "IMG") ||
    (oocf && e && e.target && e.target.tagName == "IMG")
) {
    return ddd8();
}
}
if (thji || oocf) {
document.oncontextmenu = tmvb;
} else if (ka20 || lbe8) {
window.onload = i8z9;
}
function mry2(e) {
ug4o =
    e && e.srcElement && e.srcElement != null ? e.srcElement.tagName : "";
if (ug4o != "INPUT" && ug4o != "TEXTAREA" && ug4o != "BUTTON") {
    return false;
}
}
function dlvw() {
return false;
}
if (ylp4) {
document.onselectstart = mry2;
document.ondragstart = dlvw;
}
if (document.addEventListener) {
document.addEventListener(
    "copy",
    function (e) {
    ug4o = e.target.tagName;
    if (ug4o != "INPUT" && ug4o != "TEXTAREA") {
        e.preventDefault();
    }
    },
    false
);
document.addEventListener(
    "dragstart",
    function (e) {
    e.preventDefault();
    },
    false
);
}
function sxjd(evt) {
if (evt.preventDefault) {
    evt.preventDefault();
} else {
    evt.keyCode = 37;
    evt.returnValue = false;
}
}
var q2ic = 1;
var xb5u = 2;
var vl99 = 4;
var x09i = new Array();
x09i.push(new Array(xb5u, 65));
x09i.push(new Array(xb5u, 67));
x09i.push(new Array(xb5u, 80));
x09i.push(new Array(xb5u, 83));
x09i.push(new Array(xb5u, 85));
x09i.push(new Array(q2ic | xb5u, 73));
x09i.push(new Array(q2ic | xb5u, 74));
x09i.push(new Array(q2ic, 121));
x09i.push(new Array(0, 123));
function ze7t(evt) {
evt = evt ? evt : event ? event : null;
if (evt) {
    var zaht = evt.keyCode;
    if (!zaht && evt.charCode) {
    zaht = String.fromCharCode(evt.charCode)
        .toUpperCase()
        .charCodeAt(0);
    }
    for (var hv3u = 0; hv3u < x09i.length; hv3u++) {
    if (
        evt.shiftKey == ((x09i[hv3u][0] & q2ic) == q2ic) &&
        (evt.ctrlKey | evt.metaKey) == ((x09i[hv3u][0] & xb5u) == xb5u) &&
        evt.altKey == ((x09i[hv3u][0] & vl99) == vl99) &&
        (zaht == x09i[hv3u][1] || x09i[hv3u][1] == 0)
    ) {
        sxjd(evt);
        break;
    }
    }
}
}
if (document.addEventListener) {
document.addEventListener("keydown", ze7t, true);
document.addEventListener("keypress", ze7t, true);
} else if (document.attachEvent) {
document.attachEvent("onkeydown", ze7t);
}
