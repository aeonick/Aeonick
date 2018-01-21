function scroll( fn ) {  
    var beforeScrollTop = Math.abs(document.body.scrollTop),  
        fn = fn || function() {};  
    window.addEventListener("scroll", function() {  
        var afterScrollTop = Math.abs(document.body.scrollTop),  
            delta = afterScrollTop - beforeScrollTop;  
        if( delta === 0 ) return false;  
        fn( delta > 0 ? "down" : "up" );  
        beforeScrollTop = afterScrollTop;  
    }, false);  
}
function siteTime(){
window.setTimeout("siteTime()", 1000);
var days = 3600000 * 24
var today = new Date()
var t1 = Date.UTC(2016,8,21,18,24,41)
var t2 = Date.UTC(today.getFullYear(),today.getMonth(),today.getDate(),today.getHours(),today.getMinutes(),today.getSeconds())
var diff = t2-t1
var diffDays = Math.floor((diff/days))
var diffHours = Math.floor((diff-(diffDays)*days)/3600000)
var diffMinutes = Math.floor((diff-(diffDays)*days-diffHours*3600000)/60000)
var diffSeconds = Math.floor((diff-(diffDays)*days-diffHours*3600000-diffMinutes*60000)/1000)
document.getElementById("time").innerHTML="\u672c\u535a\u5ba2\u5df2\u4e0d\u7a33\u5b9a\u8fd0\u884c "+diffDays+" \u5929 "+diffHours+" \u65f6 "+diffMinutes+" \u5206 "+diffSeconds+" \u79d2"
}

function confirm1() {
    var content=$("#content").val();
    if(!content)
    {$("#content").attr("placeholder","写上内容再提交吧~");
    return false;} 
    var author=$("#author").val();
    var bid=$("#content").attr("bid");
    var rid=$("#content").attr("rid");
    var form= {
        'content': content,
        'author': author,
        'bid': bid,
        'rid': rid
    }
    $.post("/post/comment",form,function(data){console.log(data);});
    window.location.reload(true);
    return false;
};
function confirm5() {
    var content=$("#content").val();
    if(!content)
    {$("#content").attr("placeholder","写上内容再提交吧~");
    return false;} 
};
function confirm0() {
    if(!$("#title").val()){alert("标题为空");return false;} 
    $.post("/post/article",$("#article").serialize(),function(data){window.location.href='/article/'+data;});
    alert("已提交，请稍等片刻");
    return false;
};

function confirm2() {
    var content=$("#content").val();
    if(!content)
    {$("#content").attr("placeholder","写上内容再提交吧~");
    return false;} 
    var author=$("#author").val();
    var form= {
        'content': content,
        'author': author,
        'bid': 0,
        'rid': ''
    }
    $.post("/post/comment",form,function(data){console.log(data);});
    window.location.reload(true);
    return false;
};

function confirm3() {
    var content=$("#contents").val();
    var author=$("authors").val();
    var form= {
        'content': content,
        'author': author,
        'bid': -1,
        'rid': ''
    }
    $.post("/post/comment",form,function(data){console.log(data);});
    $("#flash").show();
    $("html,body").animate({scrollTop:$("#top").offset().top},400);
    $("#contentms").val('');
    $("authors").val('');
    return false;
};

function confirm4() {
    var content=$("#contentm").val();
    var author=$("authorm").val();
    var form= {
        'content': content,
        'author': author,
        'bid': -2,
        'rid': ''
    }
    $.post("/post/comment",form,function(data){console.log(data);});
    $("#flash").show();
    $("html,body").animate({scrollTop:$("#top").offset().top},400);
    $("#contentm").val('');
    $("authorm").val('');
    return false;
};
function draw(colorr) {
    var hei = $("#cvs").height();
    var wid = $("#cvs").width();
    var canvas = document.getElementById("cvs");
    if(canvas.getContext){
        canvas.width = wid; 
        canvas.height = hei;
        lst = 0.8*hei*Math.random()+0.2*hei;
        rst = 0.8*hei*Math.random();
        var ctx = canvas.getContext("2d");
        ctx.lineWidth = 1; 
        lft=2*Math.random()
        rft=2*Math.random()
        for (var i=0;i<5;i++){
        ctx.beginPath();
        lst = lst - lft*0.2*hei*Math.random()-0.05*hei;
        rst = rst + rft*0.2*hei*Math.random()+0.05*hei;
        ctx.strokeStyle = colorr[Math.floor(6*Math.random())];
        ctx.moveTo(0, lst);
        ctx.lineTo(wid, rst);
        ctx.stroke();
        ctx.closePath();
        }
    }
};
$(document).ready(function() {
    if (document.body.clientHeight > $("#footer").offset().top + $("#footer").height() ) {
    $("#footer").css({"position":"absolute"});
    } else {
    $("#footer").css({"position":"relative"});
    }
    siteTime()
    $("#nav").click(function(){
        $(this).css("opacity","0.8");
    });
    scroll(function(dire) {
        if( dire == "down" )
        {
            $("#nav").hide();
            $("#nav").css("opacity","0.4");
        }
        if( dire == "up" )
        {
            $("#nav").show();
        }
    });
    var colorr = ['#40E0D0','#B0C4DE','#00BFFF','#8470FF','#EEEE00','#FF8C00'];
    draw(colorr);
    $("#cvs").click(function () {
        draw(colorr);
    });
    $("#navcate").click(function () {
        $("#nbtns").toggle(400);
    });
    $("pre.article img").click(function(){
        $("#mask").fadeIn(200);
        var imgsrc = $(this).attr("src");
        document.getElementById("mask").innerHTML='<span></span><a target="_blank" href="'+imgsrc+'"><img title="点击查看原图" src="'+imgsrc+'"></a>';
    });
    $("#mask").click(function(){
        $("#mask").fadeOut(200);
    });
})
$(document).ready(function() {
    $("#imgc").click(function(){
        var re=/src="(.*?)"/ig;
        var data=$('#editor').val();
        var pos=data.match(re);
        document.getElementById('imgbox').innerHTML='';
        for(var aimg in pos){document.getElementById('imgbox').innerHTML+='<div class="ibox"><img '+pos[aimg]+'/></div>';}
    });
    $("#imgd").click(function(){
        document.getElementById('imgbox').innerHTML='';
        $("#img0").val("");
    });
    $("#imgbox").on("click","img",function(){
        var addi = '<center><img src="'+$(this).attr("src")+'" /></center>';
        $("#img0").val(addi);
    });
    $("reply").click(function(){
        $("#content").attr("placeholder","回复"+$(this).attr("aid")+"的评论，刷新页面撤销");
        $("#rid").val($(this).attr("rid"));
    });
    $("button.del").click(function(){
        $(this).next().toggle(300);
    });
    $("button.quit").click(function(){
        $(this).parent().hide(300);
    });
    $("button.confirm").click(function(){
        $.post("/del/comment",{'cid':$(this).attr('cid')},function(data){console.log(data);});
        window.location.reload(true);
        return false;
    });
    $("button.bconfirm").click(function(){
        $.post("/del/article",{'bid':$(this).attr('bid')},function(data){console.log(data);});
        window.location.reload(true);
        return false;
    });
})

window.onresize=function(){$("#nbtns").css({'display':'inline-block'});};