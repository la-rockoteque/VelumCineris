import{w as s,f as c,j as t}from"./iframe-v_xVpIIQ.js";import{S as i}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const d={title:"Components/MultiSelect",component:s,args:{value:"",options:[],onChange:()=>{}}},e={render:()=>{const[n,l]=c.useState("Fire, Cold");return t.jsx(i,{children:t.jsx(s,{value:n,options:["Fire","Cold","Force","Necrotic"],onChange:l,placeholder:"Pick tags"})})}};var r,o,a;e.parameters={...e.parameters,docs:{...(r=e.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("Fire, Cold");
    return <StoryFrame>
        <MultiSelect value={value} options={["Fire", "Cold", "Force", "Necrotic"]} onChange={setValue} placeholder="Pick tags" />
      </StoryFrame>;
  }
}`,...(a=(o=e.parameters)==null?void 0:o.docs)==null?void 0:a.source}}};const S=["Default"];export{e as Default,S as __namedExportsOrder,d as default};
