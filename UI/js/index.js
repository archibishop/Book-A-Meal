inames = []
iqtyp = []
iprice = []



function addItem(x){
    inames.push(document.getElementById(x).innerHTML)
    iqtyp.push(document.getElementById('Thing1').value)
    iprice.push(parseInt(document.getElementById('testValue1').innerHTML))
    displayCart()  
}

function displayCart(){
    cartdata = '<div class="row">';

    total = 0;
    qty = 0;

    for(i = 0; i < inames.length ; i++){
        total += iqtyp[i] * iprice[i];
        cartdata += '<div class="colt1"><p><button class="buttons" onclick='+'delElement("'+ i +'")>Delete</button></p></div>'
        cartdata += '<div class="colt1"><p id="dishname1">'+ inames[i] +' </p></div>' +
                    '<div class="colt2"><p>Price : <span id="testValue1" name="testValue1">'+iprice[i]+'</span></p><p>Quantity : <span name="testVal1">'+iqtyp[i]+'</span></p></div>' 
                                
    }

    
    cartdata +=  '</div>'
    cartdata += '<div><p>Final Total: '+ total +'</p></div>'

    document.getElementById('cart').innerHTML = cartdata
}

function delElement(a){
    inames.splice(a, 1);
    iqtyp.splice(a, 1)
    iprice.splice(a, 1)
    displayCart()
}

window.onload = function () {
    
    /* event listener */
    demos = document.getElementsByName("Thing");
    tests = document.getElementsByName("testValue1");
    tests1 = document.getElementsByName("testVal1");

    for (var i = 0; i < demos.length; i++) {
        demos[i].addEventListener('change', doThing);
        demos[i].trackid = i;
    }


    /* function */
    function doThing(){
       tests[this.trackid].innerHTML = this.value * 4000
       tests1[this.trackid].innerHTML = this.value
    }
    
}