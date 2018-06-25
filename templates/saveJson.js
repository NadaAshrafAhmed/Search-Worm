//var obj = { a : 5, b : 2};
//localStorage.setItem('myObj', JSON.stringify(obj));
var obj2 = JSON.parse(localStorage.getItem('myObj'));
console.log(obj2);