//curpage
let curp=window.location.pathname.split('/');
curp=parseInt(curp[2]) || 0;



new Vue({
    delimiters: ['${', '}'],
    el: "#edit",
    data:{cates:[],title:'',img:'',abstract:''},
    methods: {
        post: function(){
            var _this=this;
            id=curp;
            title=this.$refs.title.value;
            abstract=this.$refs.abstract.value;
            tag=this.$refs.tag.value;
            img=this.$refs.img.value;
            file=this.$refs.file.value;
            content=editor.txt.html();
            Vue.http.post('/api/postarticle',{id:id,title:title,img:img,abstract:abstract,tags:tag,file:file,content:content},{emulateJSON:true}).then(function(res){
                if(res.body==1){
                    window.location.href="/";
                }
            }, function(){})
        },
        createAbs:function(){
            raw=editor.txt.html();
            raw=raw.replace(/&nbsp;/g," ");
            raw=raw.replace(/<\/p>/g,"\n");
            raw=raw.replace(/<br>/g,"\n");
            raw=raw.replace(/<.*>/g,"\n");
            raw=raw.replace(/\n\n/g,"\n");
            raw=raw.replace(/\n\n/g,"\n");
            raw=raw.replace(/\n\n/g,"\n");
            abst=raw.slice(0,150)+"...";
            this.$refs.abstract.value=abst;
        }
    },
    mounted(){
        let _this=this;
        Vue.http.get('/api/getinfo').then(function(res){
            _this.cates = res.body.cates;
            _this.$refs.file.value=_this.$refs.file.getAttribute('file');
        }, function(){})
    }
})