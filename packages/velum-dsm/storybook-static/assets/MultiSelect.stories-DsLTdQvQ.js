import{j as r}from"./jsx-runtime-Bll8AAhy.js";import{r as c}from"./index-hZsgmmNh.js";import{M as s}from"./VelumProvider-Cnx-m3OC.js";import{S as i}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const F={title:"Components/MultiSelect",component:s,args:{value:"",options:[],onChange:()=>{}}},e={render:()=>{const[n,l]=c.useState("Fire, Cold");return r.jsx(i,{children:r.jsx(s,{value:n,options:["Fire","Cold","Force","Necrotic"],onChange:l,placeholder:"Pick tags"})})}};var t,o,a;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("Fire, Cold");
    return <StoryFrame>
        <MultiSelect value={value} options={["Fire", "Cold", "Force", "Necrotic"]} onChange={setValue} placeholder="Pick tags" />
      </StoryFrame>;
  }
}`,...(a=(o=e.parameters)==null?void 0:o.docs)==null?void 0:a.source}}};const C=["Default"];export{e as Default,C as __namedExportsOrder,F as default};
