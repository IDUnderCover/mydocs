function fade(){
    divs = document.getElementsByClassName('slide')
    divs[0].style.display="none"
    }

function show(){
    divs = document.getElementsByClassName('slide')
    for(var i=0; i<divs.length; i++ ){
        divs[i].style.display="inline"
        }
    }

var count = 0

function change(index){
    divs = document.getElementsByClassName('slide');
    var index_show = (index + 1 ) % 3;
    if(index == -1){
        count = count + 1;    
        index_show = count % 3;
    }
    for(var i=0; i< divs.length; i++){
        if (i == index_show ){
                divs[i].style.display="inline";
            }
            else{
                divs[i].style.display="none";
                }
            }
    }
    

function changeOnInterval(){
    setInterval("change(-1)",2000)    
}



