function GameSession() {
    this.coins = 0
    this.click_power = 1
    this.str_boosts = []
    this.int_boosts = []
    this.init = function() {
        getCore().then(core => {
            this.coins = core.coins
            this.click_power = core.click_power
            this.str_boosts = core.str_boosts
            this.int_boosts = core.int_boosts
            render()
        })
    }
    this.add_coins = function(coins) {
        this.coins += coins
        this.coins = this.coins > 1000000000 ? 1000000000 : this.coins
    }
    this.upgrade_str_boost = function(boost_id) {
        let {boost, index} = this.get_boost(boost_id, 'str')
        if (boost) {
            if (this.coins < boost['cur_price'] || !boost['buyable']){
                return false
            }
            this.coins -= boost['cur_price']
            boost['level'] += 1
            boost['cur_power'] = boost['powers'][boost['level']]
            boost['cur_price'] = boost['price'][boost['level']]
            boost['cur_level_name'] = boost['level_names'][boost['level']]
            this.click_power += boost['cur_power']
            this.check_for_buyable()
            this.str_boosts[index] = boost
            update_str_boost(boost_id, index)
            render()
        }
    }
    this.upgrade_int_boost = function(boost_id) {
        let {boost, index} = this.get_boost(boost_id, 'int')
        if (boost) {
            if (this.coins < boost['cur_price'] || !boost['buyable']){
                return false
            }
            this.coins -= boost['cur_price']
            boost['level'] += 1
            boost['cur_interval'] = boost['auto_click_intervals'][boost['level']]
            boost['cur_price'] = boost['price'][boost['level']]
            boost['cur_level_name'] = boost['level_names'][boost['level']]
            this.check_for_buyable()
            this.int_boosts[index] = boost
            clear_timer()
            for (let id=0; id < this.int_boosts.length; id++){
                start_timer(this.int_boosts[id]['cur_interval'])
            }
            update_int_boost(boost_id, index)
            render()
        }
    }
    this.get_boost = function(boost_id, boost_type) {
        let boosts_list = boost_type == 'str' ? this.str_boosts : this.int_boosts
        for (let i = 0; i<boosts_list.length; i++){
            if (boost_id == boosts_list[i]['id']){
                return {boost: boosts_list[i], index: i}
            }
        }
        return false
    }
    this.check_for_buyable = function () {
        for (let i=0; i<this.str_boosts.length; i++){
            this.str_boosts[i]['buyable'] = this.coins >= this.str_boosts[i]['cur_price'] &&
                this.str_boosts[i]['cur_price'] != -1
            let boost = document.getElementById(`str-boost-${this.str_boosts[i]['id']}`)
            let boost_name = boost.querySelector('#new-level')
            boost_name.style.opacity = this.str_boosts[i]['buyable'] ? 1 : 0
            update_str_prices(this.str_boosts[i]['id'], i)
        }
        for (let i=0; i<this.int_boosts.length; i++){
            this.int_boosts[i]['buyable'] = this.coins >= this.int_boosts[i]['cur_price'] &&
                this.int_boosts[i]['cur_price'] != -1
            let boost = document.getElementById(`int-boost-${this.int_boosts[i]['id']}`)
            let boost_name = boost.querySelector('#new-level')
            boost_name.style.opacity = this.int_boosts[i]['buyable'] ? 1 : 0
            update_int_prices(this.int_boosts[i]['id'], i)
        }
    }
    this.toJSON = function () {
        return {'coins': this.coins,
                'click_power': this.click_power,
                'str_boosts': this.str_boosts,
                'int_boosts': this.int_boosts
        }
    }
}

let Game = new GameSession()

function getCore() {
    return fetch('/core/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        return response.core
    }).catch(error => console.log(error))
}

function call_click(isAuto) {
    if (!isAuto){
        let button = document.getElementById('clicker-button')
        change_button_pos()
    }

    Game.add_coins(Game.click_power)
    render()
}

function change_button_pos() {
    const availableScreenWidth = window.screen.availWidth
    const availableScreenHeight = window.screen.availHeight
    let button = document.getElementById('clicker-button')
    button.style.left = ((0.05 + Math.random() * 0.6) * availableScreenWidth).toString()+'px'
    button.style.top = ((0.1 + Math.random() * 0.6) * availableScreenHeight).toString()+'px'
}

function render() {
    const coinsNode = document.getElementById('coins')
    const clickNode = document.getElementById('click-power')
    Game.check_for_buyable()
    coinsNode.innerHTML = Game.coins + ' кадуш'
    clickNode.innerHTML = Game.click_power
}

function update_str_boost(boost_id, index) {
    let boost_node = document.getElementById(`str-boost-${boost_id}`)
    let boost_float_window = document.querySelector(`#str-boost-${boost_id}+.float-window`)
    boost_float_window.querySelector('.boost-level').innerText = `Текущий уровень: ${Game.str_boosts[index]['level']} (${Game.str_boosts[index]['cur_level_name']})`
    //boost_node.querySelector('#str-boost-price').innerText = Game.str_boosts[index].cur_price
    let level_bar = boost_node.querySelector('.level-bar')
    level_bar.querySelector('#segment-1').style.opacity = Game.str_boosts[index]['level'] >= 1 ? 1 : 0.2
    level_bar.querySelector('#segment-2').style.opacity = Game.str_boosts[index]['level'] >= 2 ? 1 : 0.2
    level_bar.querySelector('#segment-3').style.opacity = Game.str_boosts[index]['level'] >= 3 ? 1 : 0.2
}

function update_int_boost(boost_id, index) {
    let boost_node = document.getElementById(`int-boost-${boost_id}`)
    let boost_float_window = document.querySelector(`#int-boost-${boost_id}+.float-window`)
    boost_float_window.querySelector('.boost-level').innerText =`Текущий уровень: ${Game.int_boosts[index]['level']} (${Game.int_boosts[index]['cur_level_name']})`
    //boost_node.querySelector('#int-boost-price').innerText = Game.int_boosts[index].cur_price
    let level_bar = boost_node.querySelector('.level-bar')
    level_bar.querySelector('#segment-1').style.opacity = Game.int_boosts[index]['level'] >= 1 ? 1 : 0.2
    level_bar.querySelector('#segment-2').style.opacity = Game.int_boosts[index]['level'] >= 2 ? 1 : 0.2
    level_bar.querySelector('#segment-3').style.opacity = Game.int_boosts[index]['level'] >= 3 ? 1 : 0.2
}
function get_values(dict){
    let values = []
    for (let i in dict){
        values.push(dict[i])
    }
    return values.slice(0,3)
}
function update_str_prices(boost_id, index){
    let boost_float_window = document.querySelector(`#str-boost-${boost_id}+.float-window`)
    let values = get_values(Game.str_boosts[index]['price'])
    let level = Game.str_boosts[index]['level']
    let price_text = boost_float_window.querySelector('.boost-price')
    for (let i=0; i < values.length; i++){
        price_text.querySelector(`#price-${i}`).innerText = values[i]
        if (i == level) price_text.querySelector(`#price-${i}`).style.textDecoration = 'underline'
        else price_text.querySelector(`#price-${i}`).style.textDecoration = 'none'
    }


}
function update_int_prices(boost_id, index){
    let boost_float_window = document.querySelector(`#int-boost-${boost_id}+.float-window`)
    let values = get_values(Game.int_boosts[index]['price'])
    let level = Game.int_boosts[index]['level']
    let price_text = boost_float_window.querySelector('.boost-price')
    for (let i=0; i < values.length; i++){
        price_text.querySelector(`#price-${i}`).innerText = values[i]
        if (i == level) price_text.querySelector(`#price-${i}`).style.textDecoration = 'underline'
        else price_text.querySelector(`#price-${i}`).style.textDecoration = 'none'
    }
}
function buy_boost(boost, boost_id) {
    if (boost == 'str') {
        Game.upgrade_str_boost(boost_id)
    }
    if (boost == 'int') {
        Game.upgrade_int_boost(boost_id)
    }
}

let timer = setInterval(() => call_click(), 10000000000000);
let timers = [];

function clear_timer(){
    while(timers.length != 0){
        clearInterval(timers.pop())
    }
}
function start_timer(interval) {
    if (interval > 0) {
        timer = setInterval(() => call_click(true), interval)
        timers.push(timer)
    }
}

function setAutoSave() {
    setInterval(function() {
        update()
    }, 30000)
}
function update() {
    const csrftoken = getCookie('csrftoken')
    return fetch('/update/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            core: Game.toJSON()
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        return response.core
    }).catch(error => console.log(error))
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function start() {
    Game.init()
    setAutoSave()
}