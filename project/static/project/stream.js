function format_time(time){
    let t = new Date(time)
    let s = t.toLocaleDateString()+" "
    let h = t.getHours();
    let m = t.getMinutes();
    let str;
    if(h>12) {
        h -= 12;
        str = "PM";
    }else{
        str = "AM";
    }
    h = h < 10 ? "0" + h : h;
    m = m < 10 ? "0" + m : m;
    let result = s+h + ":" + m+str;
    return result;
}

function getList_f() {
    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState != 4) return
        updatePage(request)
    }
    request.open("GET", "/project/refresh-orders", true)
    request.send()
}

function wait_signal() {
    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState != 4) return
        show_signal(request)
    }
    request.open("GET", "/project/refresh-done", true)
    request.send()
}

function show_signal(request){
    if (request.status != 200) {
        displayError("Received status code = " + request.status)
        return
    }

    let response = JSON.parse(request.responseText)
    if (Array.isArray(response.order)) {
        order = response.order[0]
        let done = document.getElementById("done")
        while (done.hasChildNodes()) {
            done.removeChild(done.firstChild)
        }
        if (order.status=="CANCELLED"){
            let element = document.createElement("div")
            element.id = 'wait'
            statement = '<h1> Please wait for payment processing! </h1>'
            element.innerHTML = statement
            done.insertBefore(element,done.firstChild)   
            
        }
        else{
            let element = document.createElement("div")
            element.id = 'get'
            statement = '<h1> Payment done! </h1>'
            link = '<a href="/project/order/'+order.id+'">view order</a>'
            element.innerHTML = statement + link
            done.insertBefore(element,done.firstChild)
        }
    } else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } else {
        displayError(reponse)
    }
}
       

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updatePage(request) {
    if (request.status != 200) {
        displayError("Received status code = " + request.status)
        return
    }
    
    let response = JSON.parse(request.responseText)
    if (Array.isArray(response.orders)) {
        updateList(response)
    } else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } else {
        displayError(reponse)
    }
}


function updateList(items) {

    let list = document.getElementById("list")

    // Adds each new order
    for (let i = 0; i < items.orders.length; i++) {
        let item = items.orders[i]
        let id = "order_"+item.id
        let duplicate = document.getElementById(id)
        if (duplicate==null){
            let element = document.createElement("div")
            element.id = id
            link = '<div><a class = "order" href="/project/admin_order/'+item.id+'">'
            name = '<div class="order_left">User:'+item.first_name + " " + item.last_name+'</div>'
            let t = format_time(item.time)
            time = '<div class="order_left">$'+item.amount+'  #Ordered on '+t+'</div>'
            status = '<div class="order_left">Status:'
            if (item.status == "INPROGRESS"){
                status+='<span class="pending">'+item.status+'</span>'
            }
            else{
                status+='<span class="complete">'+item.status+'</span>'
            }
            end = '</div></a></div>'
            element.innerHTML = link+name+time+status+end
            list.insertBefore(element,list.firstChild)
        }
    }
}


function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}