let dry = document.getElementsByClassName('update-cart');
for(let i = 0;i < dry.length;i++){
dry[i].addEventListener('click',function(){
    let productid = this.dataset.product;
    let action = this.dataset.action;
    console.log('productid:',productid,'action:',action)
    if(user == 'AnonymousUser'){
        addcookietiem(productid,action)
    }
    else{
        updateuseritem(productid,action);
    }
})
}

function addcookietiem(productid,action){
    console.log('you are not logged in')
    if(action == 'add'){
        if(cart[productid] == undefined){
            cart[productid] = {'quantity':1}
        }
        else{
            cart[productid]['quantity'] += 1
        }
    }
    if(action == 'remove'){
        cart[productid]['quantity'] -= 1
        if(cart[productid]['quantity'] <= 0){
            delete cart[productid]
        }
    }
    console.log('cart:',cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function updateuseritem(productid,action){
    console.log('you are not logged in')
    let url = "/updateuseritem/"

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