/*! modernizr 3.5.0 (Custom Build) | MIT *
 * https://modernizr.com/download/?-getusermedia-smil-setclasses !*/
!function(e,t,n){function r(){return"function"!=typeof t.createElement?t.createElement(arguments[0]):o?t.createElementNS.call(t,"http://www.w3.org/2000/svg",arguments[0]):t.createElement.apply(t,arguments)}var s=[],a={_version:"3.5.0",_config:{classPrefix:"",enableClasses:!0,enableJSClass:!0,usePrefixes:!0},_q:[],on:function(e,t){var n=this;setTimeout(function(){t(n[e])},0)},addTest:function(e,t,n){s.push({name:e,fn:t,options:n})},addAsyncTest:function(e){s.push({name:null,fn:e})}},Modernizr=function(){};Modernizr.prototype=a,Modernizr=new Modernizr;var i=t.documentElement,o="svg"===i.nodeName.toLowerCase(),u={}.toString;Modernizr.addTest("smil",function(){return!!t.createElementNS&&/SVGAnimate/.test(u.call(t.createElementNS("http://www.w3.org/2000/svg","animate")))});var l="Moz O ms Webkit",f=a._config.usePrefixes?l.split(" "):[];a._cssomPrefixes=f;var c=function(t){var r,s=prefixes.length,a=e.CSSRule;if("undefined"==typeof a)return n;if(!t)return!1;if(t=t.replace(/^@/,""),r=t.replace(/-/g,"_").toUpperCase()+"_RULE",r in a)return"@"+t;for(var i=0;s>i;i++){var o=prefixes[i],u=o.toUpperCase()+"_"+r;if(u in a)return"@-"+o.toLowerCase()+"-"+t}return!1};a.atRule=c;var m=a._config.usePrefixes?l.toLowerCase().split(" "):[];a._domPrefixes=m;var p={elem:r("modernizr")};Modernizr._q.push(function(){delete p.elem});var d={style:p.elem.style};Modernizr._q.unshift(function(){delete d.style})}(window,document);