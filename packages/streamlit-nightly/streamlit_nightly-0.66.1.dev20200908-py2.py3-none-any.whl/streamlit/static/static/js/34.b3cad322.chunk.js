/*! For license information please see 34.b3cad322.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[34],{1431:function(e,t,s){"use strict";var a=s(10),i=s(237),n=s(0),o=s.n(n),r=s(1299),l=s(1651),c=s(1662);function p(e){const t=e.data,s=e.index,n=e.style,l=t[s].props,c=l.item,p=(l.overrides,Object(i.a)(l,["item","overrides"]));return o.a.createElement(r.e,Object.assign({key:c.value,style:Object(a.a)({boxSizing:"border-box",paddingTop:0,paddingBottom:0,display:"flex",alignItems:"center"},n)},p),c.label)}const u=o.a.forwardRef((e,t)=>{const s=o.a.Children.toArray(e.children);if(!s[0]||!s[0].props.item){const e=s[0]?s[0].props:{};return o.a.createElement(l.b,{$style:{height:"".concat(90,"px")},ref:t},o.a.createElement(l.a,e))}const a=Math.min(300,40*s.length);return o.a.createElement(l.b,{ref:t},o.a.createElement(c.FixedSizeList,{width:"100%",height:a,itemCount:s.length,itemData:s,itemKey:(e,t)=>t[e].props.item.value,itemSize:40},p))});u.displayName="VirtualDropdown";var d=u;s.d(t,"a",(function(){return d}))},2399:function(e,t,s){"use strict";s.r(t);var a=s(78),i=s(0),n=s.n(i),o=s(2385),r=s(9),l=s(1431);class c extends n.a.PureComponent{constructor(...e){super(...e),this.state={value:this.props.element.get("default")},this.setWidgetValue=e=>{const t=this.props.element.get("id");this.props.widgetMgr.setIntValue(t,this.state.value,e)},this.onChange=e=>{if(0===e.value.length)return void Object(r.d)("No value selected!");const t=Object(a.a)(e.value,1)[0];this.setState({value:parseInt(t.value,10)},()=>this.setWidgetValue({fromUi:!0}))},this.filterOptions=(e,t)=>e.filter(e=>e.label.toLowerCase().includes(t.toString().toLowerCase())),this.render=()=>{const e={width:this.props.width},t=this.props.element.get("label");let s=this.props.element.get("options"),a=this.props.disabled;const i=[{label:s.size>0?s.get(this.state.value):"No options to select.",value:this.state.value.toString()}];0===s.size&&(s=["No options to select."],a=!0);const r=[];return s.forEach((e,t)=>r.push({label:e,value:t.toString()})),n.a.createElement("div",{className:"Widget row-widget stSelectbox",style:e},n.a.createElement("label",null,t),n.a.createElement(o.a,{clearable:!1,disabled:a,labelKey:"label",onChange:this.onChange,options:r,filterOptions:this.filterOptions,value:i,valueKey:"value",overrides:{Dropdown:{component:l.a}}}))}}componentDidMount(){this.setWidgetValue({fromUi:!1})}}var p=c;s.d(t,"default",(function(){return p}))}}]);
//# sourceMappingURL=34.b3cad322.chunk.js.map