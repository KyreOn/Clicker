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
    }
    this.upgrade_str_boost = function(boost_id) {
        let {boost, index} = this.get_boost(boost_id, 'str')
        if (boost) {
            if (this.coins < boost['cur_price']){
                return false
            }
            this.coins -= boost['cur_price']
            boost['level'] += 1
            boost['cur_power'] = boost['powers'][boost['level']]
            boost['cur_price'] = boost['price'][boost['level']]
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
            if (this.coins < boost['cur_price']){
                return false
            }
            this.coins -= boost['cur_price']
            boost['level'] += 1
            boost['cur_interval'] = boost['auto_click_intervals'][boost['level']]
            boost['cur_price'] = boost['price'][boost['level']]
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
            document.getElementById(`str-boost-${this.str_boosts[i]['id']}`).disabled=!this.str_boosts[i]['buyable']
        }
        for (let i=0; i<this.int_boosts.length; i++){
            this.int_boosts[i]['buyable'] = this.coins >= this.int_boosts[i]['cur_price'] &&
                this.int_boosts[i]['cur_price'] != -1
            document.getElementById(`int-boost-${this.int_boosts[i]['id']}`).disabled=!this.int_boosts[i]['buyable']
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

function call_click() {
    Game.add_coins(Game.click_power)
    render()
}

function render() {
    const coinsNode = document.getElementById('coins')
    const clickNode = document.getElementById('click-power')
    Game.check_for_buyable()
    coinsNode.innerHTML = Game.coins
    clickNode.innerHTML = Game.click_power
}

function update_str_boost(boost_id, index) {
    let boost_node = document.getElementById(`str-boost-${boost_id}`)
    boost_node.querySelector('#str-boost-level').innerText = Game.str_boosts[index].level
    boost_node.querySelector('#str-boost-price').innerText = Game.str_boosts[index].cur_price
}

function update_int_boost(boost_id, index) {
    let boost_node = document.getElementById(`int-boost-${boost_id}`)
    boost_node.querySelector('#int-boost-level').innerText = Game.int_boosts[index].level
    boost_node.querySelector('#int-boost-price').innerText = Game.int_boosts[index].cur_price
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
        timer = setInterval(() => call_click(), interval)
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