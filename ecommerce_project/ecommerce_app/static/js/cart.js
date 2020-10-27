let dry = document.getElementsByClassName('add-btn');
for(let i = 0;i < dry.length;i++){
dry[i].addEventListener('click',function(){
    let productid = this.dataset.product;
    let action = this.dataset.action;
    console.log('productid:',productid,'action:',action)
    if(user == 'AnounymousUser'){
        return pass
    }
    else{
        updateuseritem(productid,action);
    }
})
}

function updateuseritem(productid,action){
    console.log('you are not logged in')
    let url = 'updateuseritem/'

    fetch(
        url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken
            },
            body:JSON.stringify({'productid':productid,'action':action})
        }
    )
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
}