import{j as a}from"./jsx-runtime-Bll8AAhy.js";import{r as m}from"./index-hZsgmmNh.js";import{N as o}from"./VelumProvider-Cnx-m3OC.js";import{S as u}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const T={title:"Components/NamedTableField",component:o,args:{value:"",keyLabel:"Title",valueLabel:"Text",onChange:()=>{}}},e={render:()=>{const[l,n]=m.useState("Trait:: Extra damage; Burst:: Pushes the target 10 feet");return a.jsx(u,{maxWidth:"1080px",children:a.jsx(o,{value:l,keyLabel:"Title",valueLabel:"Text",onChange:n})})}};var t,r,s;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("Trait:: Extra damage; Burst:: Pushes the target 10 feet");
    return <StoryFrame maxWidth="1080px">
        <NamedTableField value={value} keyLabel="Title" valueLabel="Text" onChange={setValue} />
      </StoryFrame>;
  }
}`,...(s=(r=e.parameters)==null?void 0:r.docs)==null?void 0:s.source}}};const h=["Default"];export{e as Default,h as __namedExportsOrder,T as default};
