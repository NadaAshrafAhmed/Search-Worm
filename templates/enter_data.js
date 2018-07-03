var id = location.search.split('id=')[1];

console.log(id);

document.getElementById("id").value = id;

console.log(document.getElementById("id").value);

document.getElementById("form").addEventListener('submit', function (event) {
    var x = document.getElementById("topic-list").children;
    var c = 0;
    var str = "";
    for (var i = 0; i < x.length; ++i) {
        console.log(x[i]);
        if (x[i].className.includes("active")) {
            if (str.length)
                str += '#';
            str += x[i].value;
            c += 1;
        }

    }
    if (c < 4) {
        document.getElementById("error").innerHTML = "Please select at least 4 interests";
        document.getElementById("error").style.display = "block";
        event.preventDefault();
    }
    var f = document.getElementById("form");
    var hiddenField = document.createElement("input");
    hiddenField.setAttribute("type", "hidden");
    hiddenField.setAttribute("name", "interests");
    hiddenField.setAttribute("value", str);
    f.appendChild(hiddenField);
}, false);  

for (var i = 1; i <= 10; ++i) {
    var x = document.getElementById("topic" + i);
    (function (x) {
        x.addEventListener('click', function (event) {
            if (x.className.includes("dummy")) {
                y = x.className.replace("dummy", "active");
            } else {
                y = x.className.replace("active", "dummy");
            }
            x.className = y;
        }, false);
    })(x);
}