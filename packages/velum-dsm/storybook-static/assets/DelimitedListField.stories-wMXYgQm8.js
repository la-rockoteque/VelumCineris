import{v as s,f as l,j as t}from"./iframe-v_xVpIIQ.js";import{S as d}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const c={title:"Components/DelimitedListField",component:s,args:{value:"",onChange:()=>{}}},e={render:()=>{const[n,i]=l.useState("Fire, Cold");return t.jsx(d,{maxWidth:"980px",children:t.jsx(s,{value:n,options:["Fire","Cold","Lightning","Poison"],onChange:i})})}};var o,r,a;e.parameters={...e.parameters,docs:{...(o=e.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("Fire, Cold");
    return <StoryFrame maxWidth="980px">
        <DelimitedListField value={value} options={["Fire", "Cold", "Lightning", "Poison"]} onChange={setValue} />
      </StoryFrame>;
  }
}`,...(a=(r=e.parameters)==null?void 0:r.docs)==null?void 0:a.source}}};const x=["Default"];export{e as Default,x as __namedExportsOrder,c as default};
