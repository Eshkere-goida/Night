
while(attempts--)
{
    if(isVip)
    {
         console.log("Доступ разрешен.");
    }
    else if(age>=18 && hasPass)
    {
        console.log("Доступ разрешен.")
    }
    else {
        console.log("Доступц запрещен.")
    }
}








//1
function checkAcess(age) {
    if (age>=18)
    {
        return console.log("Доступ разрешен.");
    }
    else if (age<18)
    {
        return console.log("Доступ запрещен. Слишком молод.");
    }
}
checkAcess(age);
//










//2
function multiplyTable(number) {
    for ( let i=1;i<=10;i++) {
        console.log(number+" * "+i+" = "+ number*i);
    }
}
multiplyTable(3);
// */


