import{N as l,f as u,j as a}from"./iframe-v_xVpIIQ.js";import{S as m}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const p={title:"Components/NamedTableField",component:l,args:{value:"",keyLabel:"Title",valueLabel:"Text",onChange:()=>{}}},e={render:()=>{const[o,n]=u.useState("Trait:: Extra damage; Burst:: Pushes the target 10 feet");return a.jsx(m,{maxWidth:"1080px",children:a.jsx(l,{value:o,keyLabel:"Title",valueLabel:"Text",onChange:n})})}};var t,r,s;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("Trait:: Extra damage; Burst:: Pushes the target 10 feet");
    return <StoryFrame maxWidth="1080px">
        <NamedTableField value={value} keyLabel="Title" valueLabel="Text" onChange={setValue} />
      </StoryFrame>;
  }
}`,...(s=(r=e.parameters)==null?void 0:r.docs)==null?void 0:s.source}}};const c=["Default"];export{e as Default,c as __namedExportsOrder,p as default};
