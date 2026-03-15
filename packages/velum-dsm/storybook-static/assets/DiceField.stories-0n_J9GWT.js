import{j as r}from"./jsx-runtime-Bll8AAhy.js";import{r as u}from"./index-hZsgmmNh.js";import{e as s}from"./VelumProvider-Cnx-m3OC.js";import{S as c}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const x={title:"Components/DiceField",component:s,args:{value:"",onChange:()=>{}}},e={render:()=>{const[n,m]=u.useState("3d8+2");return r.jsx(c,{children:r.jsx(s,{value:n,onChange:m})})}};var t,a,o;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("3d8+2");
    return <StoryFrame>
        <DiceField value={value} onChange={setValue} />
      </StoryFrame>;
  }
}`,...(o=(a=e.parameters)==null?void 0:a.docs)==null?void 0:o.source}}};const S=["Default"];export{e as Default,S as __namedExportsOrder,x as default};
