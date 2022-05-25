let timer = setInterval(() => call_click(), 10000000000000);
function call_click() {
    fetch('/call_click', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('str-boost').disabled = data.core.coins < data.core.str_boost.price;
        document.getElementById('int-boost').disabled = data.core.coins < data.core.int_boost.price;
        document.getElementById('coins').innerText = data.core.coins
        document.getElementById('click_power').innerText = data.core.click_power
    }).catch(error => console.log(error))
}

function int_boost(interval) {
    clearInterval(timer)
    if (interval > 0) {
        timer = setInterval(() => call_click(), interval)
    }
}

function buy_boost(boost) {
    fetch(boost, {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        document.getElementById('coins').innerText = data.core.coins
        document.getElementById('click_power').innerText = data.core.click_power
        document.getElementById('str-boost-level').innerText = data.core.str_boost.level
        document.getElementById('str-boost-price').innerText = data.core.str_boost.price
        document.getElementById('int-boost-level').innerText = data.core.int_boost.level
        document.getElementById('int-boost-price').innerText = data.core.int_boost.price
        document.getElementById('str-boost').disabled = data.core.coins < data.core.str_boost.price;
        document.getElementById('int-boost').disabled = data.core.coins < data.core.int_boost.price;
        int_boost(data.core.auto_click_interval)
    }).catch(error => console.log(error))
}

