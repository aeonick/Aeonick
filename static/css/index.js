$(document).ready(function() {
    $("#mask").click(function(){$("#bg").slideUp(2000,function(){$("#nav").show();});$("#snow").hide();$("#main").show();});
    $("#main").hide();
    $("#snow").hide();
    $("#bg").hide();
    $("#tela").hide();
    $("#chao").hide();
    $("#bg").fadeIn(1200);
    $("#tela").fadeIn(3800);
    $("#tela").mouseleave(function(){
        $("#tela").hide();
        $("#chao").fadeIn(1800);
    });
    $("#chao").mouseleave(function(){
        $("#chao").hide();
        $("#tela").fadeIn(1800);
        $("#snow").show();
    });
    $("#tela").click(function(){
        $("#tela").hide();
        $("#chao").fadeIn(1800);
    });
    $("#chao").click(function(){
        $("#chao").hide();
        $("#tela").fadeIn(1800);
        $("#snow").show();
    });
});

$(function(){
  var wh=$(window).height();
      setInterval(function(){
        var f=$(document).width();
        var e=Math.random()*f-100;//雪花的定位left值
        var o=0.1+0.6*Math.random();//雪花的透明度
        var fon=3+Math.random()*15;//雪花大小
        var l = e - 100 + 400 * Math.random();//雪花的横向位移
        var k=2000 + 5000 * Math.random();
        var html = "<div class='snow'>&#61545;<div>";
        $(html).clone().appendTo("#snow").css({
          left:e+"px",
          opacity:o,
          "font-size":fon,
        }).animate({
          top:(wh*2)+"px",
          left:l+"px",
          opacity:0.1,
        },k,"linear",function(){$(this).remove()})
      },100)
})