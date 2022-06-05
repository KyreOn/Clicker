let timer = setInterval(() => call_click(), 10000000000000);
let timers = [];
function call_click() {
    fetch('/call_click', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('coins').innerText = data.core.coins
        document.getElementById('click_power').innerText = data.core.click_power
        check_buyable(data)
    }).catch(error => console.log(error))
}
function clear_timer(){
    while(timers.length != 0){
        clearInterval(timers.pop())
    }
}
function start_timer(interval) {
    if (interval > 0) {
        timer = setInterval(() => call_click(), interval)
        timers.push(timer)
    }
}

function buy_boost(boost, boost_id) {
    fetch(`/${boost}/${boost_id}`, {
        method: 'GET',
    }).then(response => {
        if (response.ok){
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('coins').innerText = data.core.coins
        document.getElementById('click_power').innerText = data.core.click_power
        clear_timer()
        for (let id=0; id < data.core.int_boosts.length; id++){
            start_timer(data.core.int_boosts[id].cur_interval)
        }
        check_buyable(data)
    }).catch(error => console.log(error))
}

function check_buyable(data){
    for (let id=0; id < data.core.str_boosts.length; id++){
            document.getElementById(`str-boost-${data.core.str_boosts[id].id}`).disabled = !data.core.str_boosts[id].buyable
            document.getElementById(`str-boost-level-${data.core.str_boosts[id].id}`).innerText = data.core.str_boosts[id].level
            document.getElementById(`str-boost-price-${data.core.str_boosts[id].id}`).innerText = data.core.str_boosts[id].cur_price
            document.getElementById(`str-boost-price-${data.core.str_boosts[id].id}`).hidden = data.core.str_boosts[id].cur_price == -1
    }
    for (let id=0; id < data.core.int_boosts.length; id++){
        document.getElementById(`int-boost-${data.core.int_boosts[id].id}`).disabled = !data.core.int_boosts[id].buyable
        document.getElementById(`int-boost-level-${data.core.int_boosts[id].id}`).innerText = data.core.int_boosts[id].level
        document.getElementById(`int-boost-price-${data.core.int_boosts[id].id}`).innerText = data.core.int_boosts[id].cur_price
        document.getElementById(`int-boost-price-${data.core.str_boosts[id].id}`).hidden = data.core.int_boosts[id].cur_price == -1
    }
}