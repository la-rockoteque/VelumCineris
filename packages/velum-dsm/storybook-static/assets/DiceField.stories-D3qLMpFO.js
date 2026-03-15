import{D as s,f as c,j as r}from"./iframe-v_xVpIIQ.js";import{S as l}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const p={title:"Components/DiceField",component:s,args:{value:"",onChange:()=>{}}},e={render:()=>{const[n,u]=c.useState("3d8+2");return r.jsx(l,{children:r.jsx(s,{value:n,onChange:u})})}};var t,a,o;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("3d8+2");
    return <StoryFrame>
        <DiceField value={value} onChange={setValue} />
      </StoryFrame>;
  }
}`,...(o=(a=e.parameters)==null?void 0:a.docs)==null?void 0:o.source}}};const x=["Default"];export{e as Default,x as __namedExportsOrder,p as default};
