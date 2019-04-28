!function(e){var t={};function n(o){if(t[o])return t[o].exports;var r=t[o]={i:o,l:!1,exports:{}};return e[o].call(r.exports,r,r.exports,n),r.l=!0,r.exports}n.m=e,n.c=t,n.d=function(e,t,o){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(n.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)n.d(o,r,function(t){return e[t]}.bind(null,r));return o},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=17)}([function(e,t){var n;n=function(){return this}();try{n=n||new Function("return this")()}catch(e){"object"==typeof window&&(n=window)}e.exports=n},function(e,t,n){var o=n(5),r=n(12),i=n(13);e.exports=o,e.exports.update=function(e,t,n){return n||(n={}),!1!==n.events&&(n.onBeforeElUpdated||(n.onBeforeElUpdated=function(e,t){for(var o=n.events||i,r=0;r<o.length;r++){var a=o[r];t[a]?e[a]=t[a]:e[a]&&(e[a]=void 0)}var l=e.value,u=t.value;"INPUT"===e.nodeName&&"file"!==e.type||"SELECT"===e.nodeName?u||t.hasAttribute("value")?u!==l&&(e.value=u):t.value=e.value:"TEXTAREA"===e.nodeName&&null===t.getAttribute("value")&&(e.value=t.value)})),r(e,t,n)}},function(e,t,n){"use strict";e.exports=function(e){if(!(e instanceof HTMLElement))throw new TypeError("Expected an element");for(var t;t=e.lastChild;)e.removeChild(t);return e}},function(e,t,n){(function(t){var o,r=void 0!==t?t:"undefined"!=typeof window?window:{},i=n(6);"undefined"!=typeof document?o=document:(o=r["__GLOBAL_DOCUMENT_CACHE@4"])||(o=r["__GLOBAL_DOCUMENT_CACHE@4"]=i),e.exports=o}).call(this,n(0))},,function(e,t,n){var o=n(3),r=n(7),i=n(9),a="http://www.w3.org/2000/svg",l="http://www.w3.org/1999/xlink",u={autofocus:1,checked:1,defaultchecked:1,disabled:1,formnovalidate:1,indeterminate:1,readonly:1,required:1,selected:1,willvalidate:1},s="!--",f=["svg","altGlyph","altGlyphDef","altGlyphItem","animate","animateColor","animateMotion","animateTransform","circle","clipPath","color-profile","cursor","defs","desc","ellipse","feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence","filter","font","font-face","font-face-format","font-face-name","font-face-src","font-face-uri","foreignObject","g","glyph","glyphRef","hkern","image","line","linearGradient","marker","mask","metadata","missing-glyph","mpath","path","pattern","polygon","polyline","radialGradient","rect","set","stop","switch","symbol","text","textPath","title","tref","tspan","use","view","vkern"];function c(e,t,n){var r;-1!==f.indexOf(e)&&(t.namespace=a);var d=!1;if(t.namespace&&(d=t.namespace,delete t.namespace),d)r=o.createElementNS(d,e);else{if(e===s)return o.createComment(t.comment);r=o.createElement(e)}if(t.onload||t.onunload){var p=t.onload||function(){},m=t.onunload||function(){};i(r,function(){p(r)},function(){m(r)},c.caller.caller.caller),delete t.onload,delete t.onunload}for(var v in t)if(t.hasOwnProperty(v)){var h=v.toLowerCase(),g=t[v];if("classname"===h&&(h="class",v="class"),"htmlFor"===v&&(v="for"),u[h])if("true"===g)g=h;else if("false"===g)continue;"on"===h.slice(0,2)?r[v]=g:d?"xlink:href"===v?r.setAttributeNS(l,v,g):/^xmlns($|:)/i.test(v)||r.setAttributeNS(null,v,g):r.setAttribute(v,g)}return function e(t){if(Array.isArray(t))for(var n=0;n<t.length;n++){var i=t[n];if(Array.isArray(i))e(i);else{if(("number"==typeof i||"boolean"==typeof i||"function"==typeof i||i instanceof Date||i instanceof RegExp)&&(i=i.toString()),"string"==typeof i){if(r.lastChild&&"#text"===r.lastChild.nodeName){r.lastChild.nodeValue+=i;continue}i=o.createTextNode(i)}i&&i.nodeType&&r.appendChild(i)}}}(n),r}e.exports=r(c,{comments:!0}),e.exports.default=e.exports,e.exports.createElement=c},function(e,t){},function(e,t,n){var o=n(8),r=1,i=2,a=3,l=4,u=5,s=6,f=7,c=8,d=9,p=10,m=11,v=12,h=13;function g(e){return e===d||e===p}e.exports=function(e,t){t||(t={});var n=t.concat||function(e,t){return String(e)+String(t)};return!1!==t.attrToProp&&(e=o(e)),function(o){for(var w=r,N="",x=arguments.length,A=[],C=0;C<o.length;C++)if(C<x-1){var E=arguments[C+1],S=B(o[C]),T=w;T===p&&(T=c),T===d&&(T=c),T===f&&(T=c),T===l&&(T=u),T===i?"/"===N?(S.push([i,"/",E]),N=""):S.push([i,E]):S.push([0,T,E]),A.push.apply(A,S)}else A.push.apply(A,B(o[C]));var O,_=[null,{},[]],k=[[_,-1]];for(C=0;C<A.length;C++){var L=k[k.length-1][0],M=(S=A[C])[0];if(M===i&&/^\//.test(S[1])){var D=k[k.length-1][1];k.length>1&&(k.pop(),k[k.length-1][0][2][D]=e(L[0],L[1],L[2].length?L[2]:void 0))}else if(M===i){var F=[S[1],{},[]];L[2].push(F),k.push([F,L[2].length-1])}else if(M===u||0===M&&S[1]===u){for(var j,P="";C<A.length;C++)if(A[C][0]===u)P=n(P,A[C][1]);else{if(0!==A[C][0]||A[C][1]!==u)break;if("object"!=typeof A[C][2]||P)P=n(P,A[C][2]);else for(j in A[C][2])A[C][2].hasOwnProperty(j)&&!L[1][j]&&(L[1][j]=A[C][2][j])}A[C][0]===m&&C++;for(var V=C;C<A.length;C++)if(A[C][0]===c||A[C][0]===u)L[1][P]?""===A[C][1]||(L[1][P]=n(L[1][P],A[C][1])):L[1][P]=y(A[C][1]);else{if(0!==A[C][0]||A[C][1]!==c&&A[C][1]!==u){!P.length||L[1][P]||C!==V||A[C][0]!==a&&A[C][0]!==v||(L[1][P]=P.toLowerCase()),A[C][0]===a&&C--;break}L[1][P]?""===A[C][2]||(L[1][P]=n(L[1][P],A[C][2])):L[1][P]=y(A[C][2])}}else if(M===u)L[1][S[1]]=!0;else if(0===M&&S[1]===u)L[1][S[2]]=!0;else if(M===a){if(O=L[0],b.test(O)&&k.length){D=k[k.length-1][1];k.pop(),k[k.length-1][0][2][D]=e(L[0],L[1],L[2].length?L[2]:void 0)}}else if(0===M&&S[1]===r)void 0===S[2]||null===S[2]?S[2]="":S[2]||(S[2]=n("",S[2])),Array.isArray(S[2][0])?L[2].push.apply(L[2],S[2]):L[2].push(S[2]);else if(M===r)L[2].push(S[1]);else if(M!==m&&M!==v)throw new Error("unhandled: "+M)}if(_[2].length>1&&/^\s*$/.test(_[2][0])&&_[2].shift(),_[2].length>2||2===_[2].length&&/\S/.test(_[2][1])){if(t.createFragment)return t.createFragment(_[2]);throw new Error("multiple root elements must be wrapped in an enclosing tag")}return Array.isArray(_[2][0])&&"string"==typeof _[2][0][0]&&Array.isArray(_[2][0][2])&&(_[2][0]=e(_[2][0][0],_[2][0][1],_[2][0][2])),_[2][0];function B(e){var n=[];w===f&&(w=l);for(var o=0;o<e.length;o++){var b=e.charAt(o);w===r&&"<"===b?(N.length&&n.push([r,N]),N="",w=i):">"!==b||g(w)||w===h?w===h&&/-$/.test(N)&&"-"===b?(t.comments&&n.push([c,N.substr(0,N.length-1)],[a]),N="",w=r):w===i&&/^!--$/.test(N)?(t.comments&&n.push([i,N],[u,"comment"],[m]),N=b,w=h):w===r||w===h?N+=b:w===i&&"/"===b&&N.length||(w===i&&/\s/.test(b)?(N.length&&n.push([i,N]),N="",w=l):w===i?N+=b:w===l&&/[^\s"'=\/]/.test(b)?(w=u,N=b):w===l&&/\s/.test(b)?(N.length&&n.push([u,N]),n.push([v])):w===u&&/\s/.test(b)?(n.push([u,N]),N="",w=s):w===u&&"="===b?(n.push([u,N],[m]),N="",w=f):w===u?N+=b:w!==s&&w!==l||"="!==b?w!==s&&w!==l||/\s/.test(b)?w===f&&'"'===b?w=p:w===f&&"'"===b?w=d:w===p&&'"'===b?(n.push([c,N],[v]),N="",w=l):w===d&&"'"===b?(n.push([c,N],[v]),N="",w=l):w!==f||/\s/.test(b)?w===c&&/\s/.test(b)?(n.push([c,N],[v]),N="",w=l):w!==c&&w!==d&&w!==p||(N+=b):(w=c,o--):(n.push([v]),/[\w-]/.test(b)?(N+=b,w=u):w=l):(n.push([m]),w=f)):(w===i&&N.length?n.push([i,N]):w===u?n.push([u,N]):w===c&&N.length&&n.push([c,N]),n.push([a]),N="",w=r)}return w===r&&N.length?(n.push([r,N]),N=""):w===c&&N.length?(n.push([c,N]),N=""):w===p&&N.length?(n.push([c,N]),N=""):w===d&&N.length?(n.push([c,N]),N=""):w===u&&(n.push([u,N]),N=""),n}};function y(e){return"function"==typeof e?e:"string"==typeof e?e:e&&"object"==typeof e?e:n("",e)}};var b=RegExp("^("+["area","base","basefont","bgsound","br","col","command","embed","frame","hr","img","input","isindex","keygen","link","meta","param","source","track","wbr","!--","animate","animateTransform","circle","cursor","desc","ellipse","feBlend","feColorMatrix","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence","font-face-format","font-face-name","font-face-uri","glyph","glyphRef","hkern","image","line","missing-glyph","mpath","path","polygon","polyline","rect","set","stop","tref","use","view","vkern"].join("|")+")(?:[.#][a-zA-Z0-9-￿_:-]+)*$")},function(e,t){e.exports=function(e){return function(t,o,r){for(var i in o)i in n&&(o[n[i]]=o[i],delete o[i]);return e(t,o,r)}};var n={class:"className",for:"htmlFor","http-equiv":"httpEquiv"}},function(e,t,n){var o=n(3),r=n(10),i=n(11),a=Object.create(null),l="onloadid"+(new Date%9e6).toString(36),u="data-"+l,s=0;if(r&&r.MutationObserver){var f=new MutationObserver(function(e){if(!(Object.keys(a).length<1))for(var t=0;t<e.length;t++)e[t].attributeName!==u?(v(e[t].removedNodes,p),v(e[t].addedNodes,d)):m(e[t],d,p)});o.body?c(f):o.addEventListener("DOMContentLoaded",function(e){c(f)})}function c(e){e.observe(o.documentElement,{childList:!0,subtree:!0,attributes:!0,attributeOldValue:!0,attributeFilter:[u]})}function d(e,t){a[e][0]&&0===a[e][2]&&(a[e][0](t),a[e][2]=1)}function p(e,t){a[e][1]&&1===a[e][2]&&(a[e][1](t),a[e][2]=0)}function m(e,t,n){var o=e.target.getAttribute(u);!function(e,t){return!(!e||!t)&&a[e][3]===a[t][3]}(e.oldValue,o)?(a[e.oldValue]&&n(e.oldValue,e.target),a[o]&&t(o,e.target)):a[o]=a[e.oldValue]}function v(e,t){for(var n=Object.keys(a),o=0;o<e.length;o++){if(e[o]&&e[o].getAttribute&&e[o].getAttribute(u)){var r=e[o].getAttribute(u);n.forEach(function(n){r===n&&t(n,e[o])})}e[o].childNodes.length>0&&v(e[o].childNodes,t)}}e.exports=function e(t,n,r,l){return i(o.body,"on-load: will not work prior to DOMContentLoaded"),n=n||function(){},r=r||function(){},t.setAttribute(u,"o"+s),a["o"+s]=[n,r,0,l||e.caller],s+=1,t},e.exports.KEY_ATTR=u,e.exports.KEY_ID=l},function(e,t,n){(function(t){var n;n="undefined"!=typeof window?window:void 0!==t?t:"undefined"!=typeof self?self:{},e.exports=n}).call(this,n(0))},function(e,t){function n(e,t){if(!e)throw new Error(t||"AssertionError")}n.notEqual=function(e,t,o){n(e!=t,o)},n.notOk=function(e,t){n(!e,t)},n.equal=function(e,t,o){n(e==t,o)},n.ok=n,e.exports=n},function(e,t,n){"use strict";var o,r="http://www.w3.org/1999/xhtml",i="undefined"==typeof document?void 0:document,a=i?i.body||i.createElement("div"):{},l=a.hasAttributeNS?function(e,t,n){return e.hasAttributeNS(t,n)}:a.hasAttribute?function(e,t,n){return e.hasAttribute(n)}:function(e,t,n){return null!=e.getAttributeNode(t,n)};function u(e,t){var n=e.nodeName,o=t.nodeName;return n===o||!!(t.actualize&&n.charCodeAt(0)<91&&o.charCodeAt(0)>90)&&n===o.toUpperCase()}function s(e,t,n){e[n]!==t[n]&&(e[n]=t[n],e[n]?e.setAttribute(n,""):e.removeAttribute(n,""))}var f={OPTION:function(e,t){s(e,t,"selected")},INPUT:function(e,t){s(e,t,"checked"),s(e,t,"disabled"),e.value!==t.value&&(e.value=t.value),l(t,null,"value")||e.removeAttribute("value")},TEXTAREA:function(e,t){var n=t.value;e.value!==n&&(e.value=n);var o=e.firstChild;if(o){var r=o.nodeValue;if(r==n||!n&&r==e.placeholder)return;o.nodeValue=n}},SELECT:function(e,t){if(!l(t,null,"multiple")){for(var n=0,o=t.firstChild;o;){var r=o.nodeName;if(r&&"OPTION"===r.toUpperCase()){if(l(o,null,"selected")){n;break}n++}o=o.nextSibling}e.selectedIndex=n}}},c=1,d=3,p=8;function m(){}function v(e){return e.id}var h=function(e){return function(t,n,a){if(a||(a={}),"string"==typeof n)if("#document"===t.nodeName||"HTML"===t.nodeName){var l=n;(n=i.createElement("html")).innerHTML=l}else s=n,!o&&i.createRange&&(o=i.createRange()).selectNode(i.body),o&&o.createContextualFragment?h=o.createContextualFragment(s):(h=i.createElement("body")).innerHTML=s,n=h.childNodes[0];var s,h,g,b=a.getNodeKey||v,y=a.onBeforeNodeAdded||m,w=a.onNodeAdded||m,N=a.onBeforeElUpdated||m,x=a.onElUpdated||m,A=a.onBeforeNodeDiscarded||m,C=a.onNodeDiscarded||m,E=a.onBeforeElChildrenUpdated||m,S=!0===a.childrenOnly,T={};function O(e){g?g.push(e):g=[e]}function _(e,t,n){!1!==A(e)&&(t&&t.removeChild(e),C(e),function e(t,n){if(t.nodeType===c)for(var o=t.firstChild;o;){var r=void 0;n&&(r=b(o))?O(r):(C(o),o.firstChild&&e(o,n)),o=o.nextSibling}}(e,n))}function k(e){w(e);for(var t=e.firstChild;t;){var n=t.nextSibling,o=b(t);if(o){var r=T[o];r&&u(t,r)&&(t.parentNode.replaceChild(r,t),L(r,t))}k(t),t=n}}function L(o,r,a){var l,s=b(r);if(s&&delete T[s],!n.isSameNode||!n.isSameNode(t)){if(!a){if(!1===N(o,r))return;if(e(o,r),x(o),!1===E(o,r))return}if("TEXTAREA"!==o.nodeName){var m,v,h,g,w=r.firstChild,A=o.firstChild;e:for(;w;){for(h=w.nextSibling,m=b(w);A;){if(v=A.nextSibling,w.isSameNode&&w.isSameNode(A)){w=h,A=v;continue e}l=b(A);var C=A.nodeType,S=void 0;if(C===w.nodeType&&(C===c?(m?m!==l&&((g=T[m])?A.nextSibling===g?S=!1:(o.insertBefore(g,A),v=A.nextSibling,l?O(l):_(A,o,!0),A=g):S=!1):l&&(S=!1),(S=!1!==S&&u(A,w))&&L(A,w)):C!==d&&C!=p||(S=!0,A.nodeValue!==w.nodeValue&&(A.nodeValue=w.nodeValue))),S){w=h,A=v;continue e}l?O(l):_(A,o,!0),A=v}if(m&&(g=T[m])&&u(g,w))o.appendChild(g),L(g,w);else{var M=y(w);!1!==M&&(M&&(w=M),w.actualize&&(w=w.actualize(o.ownerDocument||i)),o.appendChild(w),k(w))}w=h,A=v}for(;A;)v=A.nextSibling,(l=b(A))?O(l):_(A,o,!0),A=v}var D=f[o.nodeName];D&&D(o,r)}}!function e(t){if(t.nodeType===c)for(var n=t.firstChild;n;){var o=b(n);o&&(T[o]=n),e(n),n=n.nextSibling}}(t);var M,D,F=t,j=F.nodeType,P=n.nodeType;if(!S)if(j===c)P===c?u(t,n)||(C(t),F=function(e,t){for(var n=e.firstChild;n;){var o=n.nextSibling;t.appendChild(n),n=o}return t}(t,(M=n.nodeName,(D=n.namespaceURI)&&D!==r?i.createElementNS(D,M):i.createElement(M)))):F=n;else if(j===d||j===p){if(P===j)return F.nodeValue!==n.nodeValue&&(F.nodeValue=n.nodeValue),F;F=n}if(F===n)C(t);else if(L(F,n,S),g)for(var V=0,B=g.length;V<B;V++){var R=T[g[V]];R&&_(R,R.parentNode,!1)}return!S&&F!==t&&t.parentNode&&(F.actualize&&(F=F.actualize(t.ownerDocument||i)),t.parentNode.replaceChild(F,t)),F}}(function(e,t){var n,o,r,i,a,u=t.attributes;for(n=u.length-1;n>=0;--n)r=(o=u[n]).name,i=o.namespaceURI,a=o.value,i?(r=o.localName||r,e.getAttributeNS(i,r)!==a&&e.setAttributeNS(i,r,a)):e.getAttribute(r)!==a&&e.setAttribute(r,a);for(n=(u=e.attributes).length-1;n>=0;--n)!1!==(o=u[n]).specified&&(r=o.name,(i=o.namespaceURI)?(r=o.localName||r,l(t,i,r)||e.removeAttributeNS(i,r)):l(t,null,r)||e.removeAttribute(r))});e.exports=h},function(e,t){e.exports=["onclick","ondblclick","onmousedown","onmouseup","onmouseover","onmousemove","onmouseout","ondragstart","ondrag","ondragenter","ondragleave","ondragover","ondrop","ondragend","onkeydown","onkeypress","onkeyup","onunload","onabort","onerror","onresize","onscroll","onselect","onchange","onsubmit","onreset","onfocus","onblur","oninput","oncontextmenu","onfocusin","onfocusout"]},,,,function(e,t,n){"use strict";n.r(t);var o=n(1),r=n.n(o),i=n(2),a=n.n(i);function l(){var e=f(['\n            <div class="row mb-4">\n                <div class="col-sm-10">\n                    <div class="row" id=','>\n                        <div class="col-md-6 col-sm-12">\n                            <div class="form-group">\n                                <label for="','" class="col-form-label">\n                                    Diametro de la Laguna Nro° ','\n                                </label>\n                                <input class="form-control" type="number" name="diameter" id="','" value="','"\n                                    onchange="','" required autocomplete="off">\n                            </div>\n                        </div>\n                        <div class="col-md-6 col-sm-12">\n                            <div class="form-group">\n                                <label for="','" class="col-form-label">\n                                    Profundidad de la Laguna Nro° ','\n                                </label>\n                                <input class="form-control" type="number" name="deepth" id="','" value="','"\n                                    onchange="','" required autocomplete="off">\n                            </div>\n                        </div>\n                        <div class="col-md-6 col-sm-12">\n                            <label for="','" class="col-form-label">\n                                Sistema de Cultivo Nro° ','\n                            </label>\n                            <select name="sistem_cultive" required class="form-control" onchange="','">\n                                <option ',">------------</option>\n                                <option ",'     value="mono">Mono Cultivo</option>\n                                <option ','     value="duo">Duo Cultivo</option>\n                            </select>\n                        </div>\n                        <div class="col-md-6 col-sm-12"></div>\n                        <div class="col-sm-12">\n                            <div id="id_species_','" class="row"></div>\n                        </div>\n                    </div>\n                </div>\n                <div class="col-sm-2">\n                    <button type="button" class="btn btn-danger" style="margin: 30px 0 0 0;" data-toggle="tooltip" data-placement="top"\n                        title="Eliminar Fila" onclick="','">\n                        <i class="fas fa-trash"></i>\n                    </button>\n                </div>\n            </div>\n        ']);return l=function(){return e},e}function u(){var e=f(["\n                                <option value=",">","</option>\n                            "]);return u=function(){return e},e}function s(){var e=f(['\n                    <div class="col-md-6 col-sm-12">\n                        <label class="col-form-label">\n                            Especies N° ','\n                        </label>\n                        <select name="specie" class="form-control">\n                            ',"\n                        </select>\n                    </div>               \n                "]);return s=function(){return e},e}function f(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}var c=document.querySelector("#id_new_lagoon");if(console.log(species),c){var d=[],p=function(){var e=document.querySelector("#id_data_lagoon"),t=[],n=a()(e);d.forEach(function(e,n){return t.push(v("id_hola",n,e))}),t.forEach(function(e){n.append(e)})},m=function(e){return function(t){return d[e][t.target.name]=t.target.value}},v=function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:"";return r()(l(),t,e,t+1,e,n.diameter,m(t),e,t+1,e,n.deepth,m(t),e,t+1,function(e){return function(t){var n=document.querySelector("#id_species_".concat(e));d[e][t.target.name].type=t.target.value;var o=0;switch(t.target.value){case"mono":o=1,console.log("mono");break;case"duo":o=2,console.log("duo")}for(var i=a()(n),l=0;l<o;l++)i.append(r()(s(),l+1,species.map(function(e){return r()(u(),e.id,e.name)})))}}(t),n.sistem_cultive.type?"":"selected","mono"==n.sistem_cultive.type?"selected":"","duo"==n.sistem_cultive.type?"selected":"",t,function(e){return function(){return d.splice(e,1),p()}}(t))};c.addEventListener("click",function(){return d.push({diameter:"",deepth:"",sistem_cultive:{type:"",species:[]}}),p()})}}]);