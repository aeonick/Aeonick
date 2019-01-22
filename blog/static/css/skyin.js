function getInfo(callback){
    let timestamp = Math.floor(Date.parse(new Date())/1000)
    let siteInfo
    if(window.localStorage){
        if(localStorage.infoTime>timestamp-3600){
            siteInfo=JSON.parse(localStorage.siteInfo)
            callback(siteInfo)
        }else{
            Vue.http.get('/api/getinfo').then(function(res){
                localStorage.siteInfo=JSON.stringify(res.body)
                localStorage.infoTime=timestamp
                siteInfo = res.body
                callback(siteInfo)
            }, function(){})
        }
    }else{
        Vue.http.get('/api/getinfo').then(function(res){
            siteInfo = res.body
            callback(siteInfo)
        }, function(){})
    }
}
function getNickName(){
    let preName=['梅花','黑桃','方块','红桃']
    let aftName=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    return preName[Math.floor(Math.random()*(4))]+aftName[Math.floor(Math.random()*(13))]
}
var MD5 = function(d){result = M(V(Y(X(d),8*d.length)));return result.toLowerCase()};function M(d){for(var _,m="0123456789ABCDEF",f="",r=0;r<d.length;r++)_=d.charCodeAt(r),f+=m.charAt(_>>>4&15)+m.charAt(15&_);return f}function X(d){for(var _=Array(d.length>>2),m=0;m<_.length;m++)_[m]=0;for(m=0;m<8*d.length;m+=8)_[m>>5]|=(255&d.charCodeAt(m/8))<<m%32;return _}function V(d){for(var _="",m=0;m<32*d.length;m+=8)_+=String.fromCharCode(d[m>>5]>>>m%32&255);return _}function Y(d,_){d[_>>5]|=128<<_%32,d[14+(_+64>>>9<<4)]=_;for(var m=1732584193,f=-271733879,r=-1732584194,i=271733878,n=0;n<d.length;n+=16){var h=m,t=f,g=r,e=i;f=md5_ii(f=md5_ii(f=md5_ii(f=md5_ii(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_ff(f=md5_ff(f=md5_ff(f=md5_ff(f,r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+0],7,-680876936),f,r,d[n+1],12,-389564586),m,f,d[n+2],17,606105819),i,m,d[n+3],22,-1044525330),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+4],7,-176418897),f,r,d[n+5],12,1200080426),m,f,d[n+6],17,-1473231341),i,m,d[n+7],22,-45705983),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+8],7,1770035416),f,r,d[n+9],12,-1958414417),m,f,d[n+10],17,-42063),i,m,d[n+11],22,-1990404162),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+12],7,1804603682),f,r,d[n+13],12,-40341101),m,f,d[n+14],17,-1502002290),i,m,d[n+15],22,1236535329),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+1],5,-165796510),f,r,d[n+6],9,-1069501632),m,f,d[n+11],14,643717713),i,m,d[n+0],20,-373897302),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+5],5,-701558691),f,r,d[n+10],9,38016083),m,f,d[n+15],14,-660478335),i,m,d[n+4],20,-405537848),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+9],5,568446438),f,r,d[n+14],9,-1019803690),m,f,d[n+3],14,-187363961),i,m,d[n+8],20,1163531501),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+13],5,-1444681467),f,r,d[n+2],9,-51403784),m,f,d[n+7],14,1735328473),i,m,d[n+12],20,-1926607734),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+5],4,-378558),f,r,d[n+8],11,-2022574463),m,f,d[n+11],16,1839030562),i,m,d[n+14],23,-35309556),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+1],4,-1530992060),f,r,d[n+4],11,1272893353),m,f,d[n+7],16,-155497632),i,m,d[n+10],23,-1094730640),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+13],4,681279174),f,r,d[n+0],11,-358537222),m,f,d[n+3],16,-722521979),i,m,d[n+6],23,76029189),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+9],4,-640364487),f,r,d[n+12],11,-421815835),m,f,d[n+15],16,530742520),i,m,d[n+2],23,-995338651),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+0],6,-198630844),f,r,d[n+7],10,1126891415),m,f,d[n+14],15,-1416354905),i,m,d[n+5],21,-57434055),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+12],6,1700485571),f,r,d[n+3],10,-1894986606),m,f,d[n+10],15,-1051523),i,m,d[n+1],21,-2054922799),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+8],6,1873313359),f,r,d[n+15],10,-30611744),m,f,d[n+6],15,-1560198380),i,m,d[n+13],21,1309151649),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+4],6,-145523070),f,r,d[n+11],10,-1120210379),m,f,d[n+2],15,718787259),i,m,d[n+9],21,-343485551),m=safe_add(m,h),f=safe_add(f,t),r=safe_add(r,g),i=safe_add(i,e)}return Array(m,f,r,i)}function md5_cmn(d,_,m,f,r,i){return safe_add(bit_rol(safe_add(safe_add(_,d),safe_add(f,i)),r),m)}function md5_ff(d,_,m,f,r,i,n){return md5_cmn(_&m|~_&f,d,_,r,i,n)}function md5_gg(d,_,m,f,r,i,n){return md5_cmn(_&f|m&~f,d,_,r,i,n)}function md5_hh(d,_,m,f,r,i,n){return md5_cmn(_^m^f,d,_,r,i,n)}function md5_ii(d,_,m,f,r,i,n){return md5_cmn(m^(_|~f),d,_,r,i,n)}function safe_add(d,_){var m=(65535&d)+(65535&_);return(d>>16)+(_>>16)+(m>>16)<<16|65535&m}function bit_rol(d,_){return d<<_|d>>>32-_}
function getToken(){for(res={},res.timestamp=String(Math.floor(Date.parse(new Date)/1e3)),seed=String(Math.floor(1e6*Math.random())),key=MD5(res.timestamp).slice(0,3);MD5(seed).slice(0,3)!=key;)seed=MD5(seed);return res.md5=seed,res}
//curpage
let curPagn=window.location.pathname.split('/')
let arch=window.location.pathname.split('/')
arch.pop()
arch=arch.join('/')+'/'
if(arch.length==1){arch='/page/'}
curPagn=curPagn[curPagn.length-1]
curPagn=curPagn.split('#')[0]
//canvas
new Vue({
    el: "#cvs",
    methods: {
        draw: function () {
            let colors = ['#40E0D0','#B0C4DE','#00BFFF','#8470FF','#EEEE00','#FF8C00']
            let canvas = document.getElementById("cvs")
            let hei = window.innerHeight*2
            let wid = window.innerWidth*2
            if(canvas.getContext){
                canvas.width = wid
                canvas.height = hei
                lst = 0.8*hei*Math.random()+0.2*hei
                rst = 0.8*hei*Math.random()
                let ctx = canvas.getContext("2d")
                lft=2*Math.random()
                rft=2*Math.random()
                for (let i=0;i<5;i++){
                    ctx.lineWidth = 2
                    ctx.beginPath()
                    lst = lst - lft*0.2*hei*Math.random()-0.05*hei
                    rst = rst + rft*0.2*hei*Math.random()+0.05*hei
                    ctx.strokeStyle = colors[Math.floor(6*Math.random())]
                    ctx.moveTo(0, lst)
                    ctx.lineTo(wid, rst)
                    ctx.stroke()
                    ctx.closePath()
                }
            }
        }
    },
    mounted(){this.draw()}
})
//navbar
new Vue({
    delimiters: ['${', '}'],
    el: "#nav",
    data:{cates:{},tog:0},
    methods: {
        setCates:function(info){
            this.cates=info.cates
        },
        toggle:function(){
            this.tog=1-this.tog
            document.getElementById("nav-btns").style.display=['none','block'][this.tog]
            document.getElementById("nav-btns").style.opacity=this.tog
        }
    },
    mounted(){getInfo(this.setCates)}
})
//sidebar
new Vue({
    delimiters: ['${', '}'],
    el: "#sidebar",
    data:{sidebarData:''},
    methods: {
        init:function(info){
            this.sidebarData=info.sidebar
        }
    },
    mounted(){
        getInfo(this.init);}
})
//footer
new Vue({
    delimiters: ['${', '}'],
    el: "#footer",
    data:{time:''},
    methods: {
        onShow:function(){
            window.setInterval(()=>{
                let days = 3600000 * 24
                let today = new Date()
                let t1 = Date.UTC(2016,8,21,18,24,41)
                let t2 = Date.UTC(today.getFullYear(),today.getMonth(),today.getDate(),today.getHours(),today.getMinutes(),today.getSeconds())
                let diff = t2-t1
                let diffDays = Math.floor((diff/days))
                let diffHours = Math.floor((diff-(diffDays)*days)/3600000)
                let diffMinutes = Math.floor((diff-(diffDays)*days-diffHours*3600000)/60000)
                let diffSeconds = Math.floor((diff-(diffDays)*days-diffHours*3600000-diffMinutes*60000)/1000)
                this.time=diffDays+" 天 "+diffHours+" 时 "+diffMinutes+" 分 "+diffSeconds+" 秒"
            },1000)
        }
    },
    mounted(){
        this.onShow()
    }
})
//article
let eleList = document.querySelectorAll('.artiList date')
for (let i = 0; i < eleList.length; i++) {eleList[i].innerHTML="Posted on: "+eleList[i].innerHTML.slice(0,-9);}
getInfo((info)=>{
    eleList = document.querySelectorAll('file')
    for (let i = 0; i < eleList.length; i++) {eleList[i].innerHTML=info.cates[eleList[i].innerHTML];}
})
eleList = document.querySelectorAll('tag')
for (let i = 0; i < eleList.length; i++) {
    let temp='&#61484;&nbsp;&nbsp;'
    tags=eleList[i].innerHTML.split(",")
    for (let j = 0; j < tags.length; j++) {
        temp+='<a href="/arch/'+tags[j]+'/1">&nbsp;'+tags[j]+'&nbsp;</a>'
    }
    eleList[i].innerHTML=temp
}
//pagn
eleList = document.querySelectorAll('pagn')
if(eleList.length){
    if(curPagn==""){curPagn=1;}
    if(curPagn==1){document.querySelector('pagn.prev').className += " hidden";}
    if(curPagn==eleList.length-2){document.querySelector('pagn.next').className += " hidden";}
    document.querySelector('pagn.prev').parentElement.href=arch+String(parseInt(curPagn)-1)
    document.querySelector('pagn.next').parentElement.href=arch+String(parseInt(curPagn)+1)
    for (let i = 0; i < eleList.length; i++) {
        eleList[i].parentElement.href=arch+String(i)
        if(eleList[i].innerHTML==curPagn){
            eleList[i].className += "active"
            eleList[i].parentElement.href=""
        }
    }
}
//comments
let replyId = null;
poster=new Vue({
    delimiters: ['${', '}'],
    el: "#commentpost",
    data:{textholder:'一句话吐槽',inputholder:'输入您的昵称或留空',text:'',author:'',lastTime:0},
    methods: {
        onshow: function(){},
        post: function(){
            var _this=this
            if(this.lastTime+10>Math.floor(Date.parse(new Date)/1e3)){
                _this.textholder="回复得太快了，请稍候..."
                return false
            }else if(this.text==''){
                _this.textholder="回复内容不能为空"
                return false
            }
            this.lastTime=Math.floor(Date.parse(new Date)/1e3)
            token=getToken()
            if(_this.author==''){_this.author=getNickName()}
            Vue.http.post('/api/postcomment',{author:_this.author,content:_this.text,bid:curPagn,rid:replyId,timestamp:token.timestamp,md5:token.md5},{emulateJSON:true}).then(function(res){
                if(res.body==1){
                    comments.onshow()
                    _this.author="";
                    _this.text="";
                    _this.textholder="一句话吐槽"
                    replyId=null;
                }
            }, function(){})
        },
        cancel:function(){
            replyId=null
            this.textholder="一句话吐槽"
        }
    },
    mounted(){
        this.onshow()
    }
})
Vue.component('comment', {
    delimiters: ['${', '}'],
    props: ['info'],
    template: '<div class="comment"><author>${ info.content.author }</author><a href="#tags"><reply v-on:click="reply"> 回复</reply></a><content>${ info.content.content }</content><date>${ info.content.date }</date><subcom v-for="subcom in info.content.subcom" v-bind:subcom="subcom"></subcom></div>',
    methods:{
        onshow: function(){
            this.info.content.date=String(this.info.content.date).slice(0,-7)
        },
        reply:function(){
            replyId=this.info.id
            poster.textholder="回复|"+this.info.content.author+"|的评论，双击文本框可撤销"
        }
    },
    mounted(){
        this.onshow()
    }
})
Vue.component('subcom', {
    delimiters: ['${', '}'],
    props: ['subcom'],
    template: '<div class="comment"><author>${ subcom.author }</author><content>${ subcom.content }</content><date>${ subcom.date }</date></div>',
    methods:{
        onshow: function(){
            this.subcom.date=String(this.subcom.date).slice(0,-7)
        }
    },
    mounted(){
        this.onshow()
    }
})
comments=new Vue({
    delimiters: ['${', '}'],
    el: "#comments",
    data:{infos:{}},
    methods: {
        onshow: function(){
            let _this=this
            Vue.http.post('/api/getcomment',{id:curPagn},{emulateJSON:true}).then(function(res){
                let infos=[];
                for (let i in res.body) {
                    infos.unshift({'id':i,'content':res.body[i]})
                }
                _this.infos=infos;
            }, function(){})
        }
    },
    mounted(){
        if(arch=="/article/")this.onshow()
    }
})
Vue.component('memo', {
    delimiters: ['${', '}'],
    props: ['info'],
    template: '<div class="well"><author>${ info.content.author }</author><content>${ info.content.content }</content><date>${ info.content.date }</date></div>',
    methods:{
        onshow: function(){
            this.info.content.date=String(this.info.content.date).slice(0,-13)
        }
    },
    mounted(){
        this.onshow()
    }
})
new Vue({
    delimiters: ['${', '}'],
    el: "#memopost",
    data:{textholder:'留下你的足迹',inputholder:'输入昵称或留空',text:'',author:'',lastTime:0,infos:{}},
    methods: {
        onshow: function(){
            let _this=this
            Vue.http.post('/api/getcomment',{id:0},{emulateJSON:true}).then(function(res){
                let infos=[];
                for (let i in res.body) {
                    infos.unshift({'id':i,'content':res.body[i]})
                }
                _this.infos=infos;
            }, function(){})
        },
        post: function(){
            var _this=this
            if(this.lastTime+10>Math.floor(Date.parse(new Date)/1e3)){
                _this.textholder="操作太快了，请稍候..."
                return false
            }else if(this.text==''){
                _this.textholder="内容不能为空"
                return false
            }
            this.lastTime=Math.floor(Date.parse(new Date)/1e3)
            token=getToken()
            if(_this.author==''){_this.author=getNickName()}
            Vue.http.post('/api/postcomment',{author:_this.author,content:_this.text,bid:0,rid:null,timestamp:token.timestamp,md5:token.md5},{emulateJSON:true}).then(function(res){
                if(res.body==1){
                    _this.onshow()
                    _this.author="";
                    _this.text="";
                    _this.textholder="留下你的足迹"
                    replyId=null;
                }
            }, function(){})
        }
    },
    mounted(){
        if(window.document.location.pathname=="/memo"){
            this.onshow()
        }
    }
})
new Vue({
    delimiters: ['${', '}'],
    el: "#moon",
    data:{textholder:'月池',inputholder:'署名',text:'',author:'',lastTime:0},
    methods: {
        post: function(){
            var _this=this
            if(this.lastTime+1000>Math.floor(Date.parse(new Date)/1e3)){return false}
            this.lastTime=Math.floor(Date.parse(new Date)/1e3)
            token=getToken()
            if(_this.author==''){_this.author=getNickName()}
            Vue.http.post('/api/postcomment',{author:_this.author,content:_this.text,bid:-1,rid:null,timestamp:token.timestamp,md5:token.md5},{emulateJSON:true}).then(function(res){
                if(res.body==1){
                    _this.author="";
                    _this.text="";
                    _this.textholder="许愿完成，祝你好运！"
                    replyId=null;
                }
            }, function(){})
        }
    }
})
new Vue({
    delimiters: ['${', '}'],
    el: "#sun",
    data:{textholder:'日池',inputholder:'署名',text:'',author:'',lastTime:0},
    methods: {
        post: function(){
            var _this=this
            if(this.lastTime+1000>Math.floor(Date.parse(new Date)/1e3)){return false}
            this.lastTime=Math.floor(Date.parse(new Date)/1e3)
            token=getToken()
            Vue.http.post('/api/postcomment',{author:_this.author,content:_this.text,bid:-2,rid:null,timestamp:token.timestamp,md5:token.md5},{emulateJSON:true}).then(function(res){
                if(res.body==1){
                    _this.author="";
                    _this.text="";
                    _this.textholder="许愿完成，祝你好运！"
                    replyId=null;
                }
            }, function(){})
        }
    }
})