$(document).ready(function() {
    $("#c1").click(function(){
        $(".well.big").hide();
        $("#cc1").show();
    });
    $("#c2").click(function(){
        $(".well.big").hide();
        $("#cc2").show();
    });
    $("#c4").click(function(){
        $(".well.big").hide();
        $("#cc4").show();
    });
    $("#c5").click(function(){
        $(".well.big").hide();
        $("#cc0").show();
    });
    $("#tcg0").click(function(){
        $.post("/config/tcg0",{'tcg0':$("#cg0").val()},function(data){});
    });
    $("#tcg1").click(function(){
        $.post("/config/tcg1",{'tcg1':$("#cg1").val()},function(data){});
    });
    $("#tcg2").click(function(){
        if($("#cg4").val()==$("#cg5").val()){$.post("/config/tcg2",{'old':$("#cg3").val(),'new':$("#cg4").val()},function(data){});}else{alert('密码不一致');}
    });
    $("#tcg3").click(function(){
        $.post("/config/tcg3",{'tcg3':$("#cg6").val()},function(data){});
    });
    $("#tcg4").click(function(){
        $.post("/config/tcg4",{'tcg4':$("#cg7").val()},function(data){});
    });
    $("button.cate").click(function(){
        var newId=$(this).parent().find("input.oId").val();
        var content=$(this).parent().find("input.cateContent").val();
        var oldId=$(this).attr('cid')
        $.post("/config/cate",{'oldId':oldId,'newId':newId,'content':content},function(data){});
    });
})