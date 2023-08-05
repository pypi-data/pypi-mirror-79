/*! For license information please see 28.24e9c4c4.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[28],{2198:function(e,t,a){},2395:function(e,t,a){"use strict";a.r(t);var r=a(78),n=a(15),i=a.n(n),s=a(22),c=a(0),o=a.n(c),u=a(9),h=a(233),d=a(104),g=a(2156),l=a.n(g),p=a(1609);a(2198);const f="(index)",w=new Set(["datetimeIndex","float_64Index","int_64Index","rangeIndex","timedeltaIndex","uint_64Index"]);class v extends c.PureComponent{constructor(...e){super(...e),this.vegaView=void 0,this.vegaFinalizer=void 0,this.defaultDataName="source",this.element=null,this.state={error:void 0},this.finalizeView=()=>{this.vegaFinalizer&&this.vegaFinalizer(),this.vegaFinalizer=void 0,this.vegaView=void 0},this.generateSpec=()=>{const e=this.props.element,t=JSON.parse(e.get("spec")),a=JSON.parse(e.get("useContainerWidth"));if(this.props.height?(t.width=this.props.width-38,t.height=this.props.height):a&&(t.width=this.props.width-38),t.padding||(t.padding={}),null==t.padding.bottom&&(t.padding.bottom=20),t.datasets)throw new Error("Datasets should not be passed as part of the spec");return t}}componentDidMount(){var e=this;return Object(s.a)(i.a.mark((function t(){return i.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,e.createView();case 3:t.next=8;break;case 5:t.prev=5,t.t0=t.catch(0),e.setState({error:t.t0});case 8:case"end":return t.stop()}}),t,null,[[0,5]])})))()}componentWillUnmount(){this.finalizeView()}componentDidUpdate(e){var t=this;return Object(s.a)(i.a.mark((function a(){var n,s,c,o,h,d,g,l,p,f,w,v,b,m,j,x,V;return i.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:if(n=e.element,s=t.props.element,c=n.get("spec"),o=s.get("spec"),t.vegaView&&c===o&&e.width===t.props.width&&e.height===t.props.height){a.next=15;break}return Object(u.c)("Vega spec changed."),a.prev=6,a.next=9,t.createView();case 9:a.next=14;break;case 11:a.prev=11,a.t0=a.catch(6),t.setState({error:a.t0});case 14:return a.abrupt("return");case 15:for(h=n.get("data"),d=s.get("data"),(h||d)&&t.updateData(t.defaultDataName,h,d),g=O(n)||{},l=O(s)||{},p=0,f=Object.entries(l);p<f.length;p++)w=Object(r.a)(f[p],2),v=w[0],b=w[1],m=v||t.defaultDataName,j=g[m],t.updateData(m,j,b);for(x=0,V=Object.keys(g);x<V.length;x++)v=V[x],l.hasOwnProperty(v)||v===t.defaultDataName||t.updateData(v,null,null);t.vegaView.resize().runAsync();case 23:case"end":return a.stop()}}),a,null,[[6,11]])})))()}updateData(e,t,a){if(!this.vegaView)throw new Error("Chart has not been drawn yet");if(!a||!a.get("data")){return void(this.vegaView._runtime.data.hasOwnProperty(e)&&this.vegaView.remove(e,p.truthy))}if(!t||!t.get("data"))return void this.vegaView.insert(e,j(a));const n=Object(d.h)(t.get("data")),i=Object(r.a)(n,2),s=i[0],c=i[1],o=Object(d.h)(a.get("data")),h=Object(r.a)(o,2),g=h[0];if(function(e,t,a,r,n,i){if(a!==i)return!1;if(t>n)return!1;if(0===t)return!1;const s=e.get("data"),c=r.get("data"),o=i-1,u=t-1;if(Object(d.g)(s,o,0)!==Object(d.g)(c,o,0)||Object(d.g)(s,o,u)!==Object(d.g)(c,o,u))return!1;return!0}(t,s,c,a,g,h[1]))s<g&&this.vegaView.insert(e,j(a,s));else{const t=p.changeset().remove(p.truthy).insert(j(a));this.vegaView.change(e,t),Object(u.c)("Had to clear the ".concat(e," dataset before inserting data through Vega view."))}}createView(){var e=this;return Object(s.a)(i.a.mark((function t(){var a,n,s,c,o,h,d,g,p,f,w,v,O,j,x,V;return i.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:if(Object(u.c)("Creating a new Vega view."),e.element){t.next=3;break}throw Error("Element missing.");case 3:return e.finalizeView(),a=e.props.element,n=e.generateSpec(),t.next=8,l()(e.element,n);case 8:if(s=t.sent,c=s.vgSpec,o=s.view,h=s.finalize,e.vegaView=o,e.vegaFinalizer=h,d=m(a),1===(g=d?Object.keys(d):[]).length?(p=Object(r.a)(g,1),f=p[0],e.defaultDataName=f):0===g.length&&c.data&&(e.defaultDataName="source"),(w=b(a))&&o.insert(e.defaultDataName,w),d)for(v=0,O=Object.entries(d);v<O.length;v++)j=Object(r.a)(O[v],2),x=j[0],V=j[1],o.insert(x,V);return t.next=22,o.runAsync();case 22:e.vegaView.resize().runAsync();case 23:case"end":return t.stop()}}),t)})))()}render(){if(this.state.error)throw this.state.error;return o.a.createElement("div",{className:"stVegaLiteChart",ref:e=>{this.element=e}})}}function b(e){const t=e.get("data");return t?j(t):null}function m(e){const t=O(e);if(null==t)return null;const a={};for(var n=0,i=Object.entries(t);n<i.length;n++){const e=Object(r.a)(i[n],2),t=e[0],s=e[1];a[t]=j(s)}return a}function O(e){if(!e.get("datasets")||e.get("datasets").isEmpty())return null;const t={};return e.get("datasets").forEach((e,a)=>{if(!e)return;const r=e.get("hasName")?e.get("name"):null;t[r]=e.get("data")}),t}function j(e,t=0){if(!e.get("data"))return[];if(!e.get("index"))return[];if(!e.get("columns"))return[];const a=[],n=Object(d.h)(e.get("data")),i=Object(r.a)(n,2),s=i[0],c=i[1],o=e.get("index").get("type"),u=w.has(o);for(let r=t;r<s;r++){const t={};u&&(t[f]=Object(d.f)(e.get("index"),0,r));for(let a=0;a<c;a++)t[Object(d.f)(e.get("columns"),0,a)]=Object(d.g)(e.get("data"),a,r);a.push(t)}return a}var x=Object(h.a)(v);a.d(t,"default",(function(){return x}))}}]);
//# sourceMappingURL=28.24e9c4c4.chunk.js.map