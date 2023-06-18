<script setup>
import axios from 'axios'
import { reactive } from 'vue'
import * as echarts from 'echarts/core'
import { GridComponent } from 'echarts/components'
import { LineChart } from 'echarts/charts'
import { UniversalTransition } from 'echarts/features'
import { CanvasRenderer } from 'echarts/renderers'
echarts.use([GridComponent, LineChart, CanvasRenderer, UniversalTransition])

const myData = reactive({"data":[],"cap":[],"y0":[]})

let tmp = []
for (let i = 0; i < 20; i++) {
    tmp.push('1.png')
}

const img = reactive(tmp)

for (let i = 0; i < 20; i++) {
    myData.cap.push('data['+i+']')
    myData.data.push(' ')
}
myData.cap[0] = '红外'
myData.cap[1] = '电感'
myData.cap[2] = '霍尔'
myData.cap[3] = '温度'
myData.cap[4] = '电机使能'
myData.cap[5] = '电机输出'
myData.cap[6] = '风扇使能'
myData.cap[7] = '风扇输出'
myData.cap[8] = '加热器使能'
myData.cap[9] = '加热器输出'
myData.cap[10] = '物体'
// the init button value is ‘开始’, click to change the value


let get_data = () => {
    axios.post('http://'+window.location.hostname+':5000/get',{})
        .then( (res) => {
          console.log(res.data)
        //myData.data = res.data
        //hongwai diangan huoer
        //wendu / 2048 * 100
        //wendu2 / 32768 * 100 
        //pwm0 (motor) pwm1(fan) pwm2(heater)
        //wood fe cu in0 in1 in2
          for (let i = 0; i < 3; i++){
            if (res.data[i] == 0) {
              myData.data[i] = 'off'
            } else {
                myData.data[i] = 'on'
            }
          }
          
          let value = res.data[3] / 32768 * 100
          myData.data[3] = parseFloat(value).toFixed(2)
          
          myData.data[4] = res.data[10]
          myData.data[5] = res.data[4]
          myData.data[6] = res.data[11]
          myData.data[7] = res.data[5]
          myData.data[8] = res.data[12]
          myData.data[9] = res.data[6]
          if (res.data[7] == 1){
            myData.data[10] = "木头"
          }else if (res.data[8] == 1){
            myData.data[10] = "铁"
          }else if (res.data[9] == 1){
            myData.data[10] = "铜"
          }else{
            myData.data[10] = "无"
          }
          myData.y0.push(myData.data[3])
          if (myData.y0.length > 30) {
              myData.y0.shift()
          }
          for (let i = 0; i < myData.data.length; i++) {
            if (myData.data[i] != 0 && myData.data[i] != 'off') {
                img[i] = 'ayaka.jpg'
            } else {
                img[i] = '1.png'
            }
          }
        } )
        .catch( (err) => console.log(err) );
}


let echart_draw = () => {
    var chartDom = document.getElementById('plot')
    var myChart = echarts.init(chartDom);
    var option
    var xAxisData = []
    for (var i = 0; i < 30; i++) {
        xAxisData.push(i)
    }
    option = {
    xAxis: {
        type: 'category',
        data: xAxisData
        // data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },

    yAxis: {
        type: 'value',
        min: 23,
    },
    
    series: [
        {
        // data: [820, 932, 901, 934, 1290, 1330, 1320],
        data : myData.y0,
        type: 'line',
        showSymbol: false,
        smooth: true,
        layoutAnimation: false,
        animation: false
        }
        
    ]
    };
    myChart.setOption(option);
}

let interval = setInterval(get_data, 100)
let interval2 = setInterval(echart_draw, 100)

</script>

<template>

<div class="div_out_0">
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[0] }}</span>
        </div>
        <img :src="img[0]" class="img_icon" />
        <span class="str">{{ myData.data[0] }}</span>
    </div>
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[1] }}</span>
        </div>
        <img :src="img[1]" class="img_icon" />
        <span class="str">{{ myData.data[1] }}</span>
    </div>
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[2] }}</span>
        </div>
        <img :src="img[2]" class="img_icon" />
        <span class="str">{{ myData.data[2] }}</span>
    </div>
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[3] }}</span>
        </div>
        <img :src="img[3]" class="img_icon" />
        <span class="str">{{ myData.data[3] }}</span>
    </div>
</div>

<div class="div_out">
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[4] }}</span>
        </div>
        <img :src="img[4]" class="img_icon" />
        <span class="str">{{ myData.data[4] }}</span>
    </div>
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[5] }}</span>
        </div>
        <img :src="img[5]" class="img_icon" />
        <span class="str">{{ myData.data[5] }}</span>
    </div>
</div>

<div class="div_out">
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[6] }}</span>
        </div>
        <img :src="img[6]" class="img_icon" />
        <span class="str">{{ myData.data[6] }}</span>
    </div>
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[7] }}</span>
        </div>
        <img :src="img[7]" class="img_icon" />
        <span class="str">{{ myData.data[7] }}</span>
    </div>
</div>

<div class="div_out">
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[8] }}</span>
        </div>
        <img :src="img[8]" class="img_icon" />
        <span class="str">{{ myData.data[8] }}</span>
    </div>
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap">{{ myData.cap[9] }}</span>
        </div>
        <img :src="img[9]" class="img_icon" />
        <span class="str">{{ myData.data[9] }}</span>
    </div>
</div>

<div class="div_out_2">
    <div class="div_cap">
        <div class="cap2">    
            <label for="temperature">设定温度:</label>
            <input type="range" id="temperature" name="temperature" min="20" max="50" v-model="temperature" @input="updateTemperature">
        </div>
        <span class="str">{{ temperature }}</span>
    </div>
</div>

<div class="div_out_2">
    <div class="div_inline">
        <div class="div_cap">
            <span class="cap2">{{ myData.cap[10] }}</span>
        </div>
        <img :src="img[10]" class="img_icon" />
        <span class="str">{{ myData.data[10] }}</span>
    </div>
        <div class="div_inline">
        <div class="div_cap">
            <span class="cap2">{{ "计数：" }}</span>
        </div>
        <img :src="img[10]" class="img_icon" />
        <span class="str">{{ 0 }}</span>
    </div>
</div>

<div class="div">
    <div class="div_inline">
        <button @click="start_botton" id="botton">{{botton_value.start}}</button>
        <!-- to realize 3 class for normal hover and click -->
            
    </div>
</div>

<div class="div">
    <div class="div_inline">
        <button @click="motor_botton" class="botton_2">{{botton_value.motor}}</button>
    </div>
    <div class="div_inline">
        <button @click="heat_botton" class="botton_2">{{botton_value.heat}}</button>
    </div>
</div>

<div class="div">
    <div class="div_inline">
        <button @click="relay1_botton" class="botton_2">{{botton_value.relay1}}</button>
    </div>
    <div class="div_inline">
        <button @click="relay2_botton" class="botton_2">{{botton_value.relay2}}</button>
    </div>
</div>



<div class="div">
    <div class="div_inline">
        <span class="cap_en">{{ "temperature's plot" }}</span>
    </div>
    <!-- <div class="div_inline">
        <span class="cap">{{ "证明我可以显示中文" }}</span>
    </div> -->
</div>

<div class="Echart">
    <div id="plot"></div>
</div>


</template>

<script>
const botton_value = reactive({"start":'开始',"motor":'启动电机',"heat":'启动加热',"relay1":'启动继电器1',"relay2":'启动继电器2'})
const int_value = reactive({"temperature":25})
let send_data = () => {
    let sendData = {
        "start":botton_value.start != '开始',
        "motor":botton_value.motor != '启动电机',
        "heat":botton_value.heat != '启动加热',
        "relay1":botton_value.relay1 != '启动继电器1',
        "relay2":botton_value.relay2 != '启动继电器2',
        "temperature":int_value.temperature
    }
    axios.post('http://'+window.location.hostname+':5000/set',sendData)
        .then( (res) => {
          console.log(res.data)
        } )
        .catch( (err) => console.log(err) );
}
let start_botton = ()=>{
    if (botton_value.start == '开始') {
        botton_value.start = '停止'
    } else {
        botton_value.start = '开始'
    }
    send_data()
}
let motor_botton = ()=>{
    if (botton_value.motor == '启动电机') {
        botton_value.motor = '停止电机'
    } else {
        botton_value.motor = '启动电机'
    }
    send_data()
}
let heat_botton = ()=>{
    if (botton_value.heat == '启动加热') {
        botton_value.heat = '停止加热'
    } else {
        botton_value.heat = '启动加热'
    }
    send_data()
}
let relay1_botton = ()=>{
    if (botton_value.relay1 == '启动继电器1') {
        botton_value.relay1 = '收回继电器1'
    } else {
        botton_value.relay1 = '启动继电器1'
    }
    send_data()
}
let relay2_botton = ()=>{
    if (botton_value.relay2 == '启动继电器2') {
        botton_value.relay2 = '收回继电器2'
    } else {
        botton_value.relay2 = '启动继电器2'
    }
    send_data()
}
  window.addEventListener('DOMContentLoaded', () => {
    const myButton = document.getElementById('botton');

    myButton.addEventListener('mouseenter', () => {
      myButton.classList.add('hover');
    });

    myButton.addEventListener('mouseleave', () => {
      myButton.classList.remove('hover');
    });

    myButton.addEventListener('mousedown', () => {
      myButton.classList.add('active');
    });

    myButton.addEventListener('mouseup', () => {
      myButton.classList.remove('active');
    });
  });
  export default {
  data() {
    return {
      temperature: 25
    }
  },
  methods: {
    updateTemperature() {
      console.log(`Temperature updated to ${this.temperature}`);
      int_value.temperature = this.temperature;
      send_data();
    }
  },
  computed: {
    externalTemperature() {
      return this.temperature;
    }
  }
}
</script>

<style>

 #botton {
    background-color: #007ac5;
    border: none;
    color: white;
    padding: 1em;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 1.5em;
    margin: 0.5em;
    cursor: pointer;
    border-radius: 0.5em;
}
  #button:hover {
    /* background-color: #283593; */
    background-color: #e9e9e9;
    }
 
  #button:active {
    background-color: #1a237e;
    }
  
.botton_2 {
    background-color: #008a20;
    border: none;
    color: white;
    padding: 0.5em;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 1em;
    margin: 0.5em;
    cursor: pointer;
    border-radius: 0.5em;
}

.str {
    font-family: 'Times New Roman', Times, serif;
    /* font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif; */
    color: #252525;
    margin-left: 1em;
}

.cap_en {
    font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
    /* font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif; */
    color: #0060af;
    margin-left: 0.5em;
    font-size: large;
}

.cap {
    font-family: 'KaiTi', Times, serif;
    /* font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif; */
    color: #0060af;
    margin-left: 0.5em;
    font-size: large;
}

.cap2 {
    font-family: 'KaiTi', Times, serif;
    /* font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif; */
    color: #6ebeff;
    margin-left: 0.5em;
    font-size: large;
}

.div_out {
    font-size: x-large;
    margin: auto;
    background-color: #81bfec;
    text-align: center;
}
.div_out_0 {
    font-size: x-large;
    margin: auto;
    background-color: #98d3fe;
    text-align: center;
}
.div_out_2 {
    font-size: x-large;
    margin: auto;
    background-color: #0075b4;
    text-align: center;
}

.div_cap {
    font-size: large;
    margin: auto;
    text-align: center;
}

.div {
    font-size: x-large;
    margin: auto;
    background-color: #ffffff;
    text-align: center;
}

.img_icon {
    height: 1em;
    margin-top: 0.5em;
}

.div_inline {
    display: inline-block;
    margin: 1.5em;
} 


#plot {
    max-width: 600px;
    width: 100%;
    height:400px;
    margin: auto;
    margin-top: 10px
  }

</style>
