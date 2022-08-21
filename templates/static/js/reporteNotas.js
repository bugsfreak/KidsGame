function Sub(){
    var n, k, r, e, v, sum, avg;
    n=(document.getElementById('aname').value);
    k=parseFloat(document.getElementById('am').value);
    r=parseFloat(document.getElementById('aj').value);
    e=parseFloat(document.getElementById('ad').value);
    v=parseFloat(document.getElementById('an').value);
    // Calculating Total
    sum=k+r+e+v;
    avg=sum/4;
    // Display on Student Data
    var newTable = document.getElementById('TableScore');
    var row = newTable.insertRow(-1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(0);
    var cell3 = row.insertCell(0);
    var cell4 = row.insertCell(0);

    cell4.innerHTML= n;
    cell3.innerHTML=sum;
    cell2.innerHTML = avg;

    if(avg>=7){
        cell1.innerHTML="<font color=green>Aprobado</font>";
    }else{
        cell1.innerHTML="<font color=red>Reprobado</font>";
    }
}