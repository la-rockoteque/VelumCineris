import{j as a}from"./jsx-runtime-Bll8AAhy.js";import{r as i}from"./index-hZsgmmNh.js";import{T as o}from"./VelumProvider-Cnx-m3OC.js";import{S as c}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const v={title:"Components/TabBar",component:o,args:{items:[],activeKey:"",onChange:()=>{},ariaLabel:"Tabs"}},p=[{key:"compendium",label:"Compendium"},{key:"details",label:"Details"},{key:"translator",label:"Translator"},{key:"image",label:"Image"}],e={render:()=>{const[m,n]=i.useState("compendium");return a.jsx(c,{maxWidth:"980px",children:a.jsx(o,{ariaLabel:"Workspace tabs",items:p,activeKey:m,onChange:n})})}};var t,r,s;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => {
    const [active, setActive] = useState("compendium");
    return <StoryFrame maxWidth="980px">
        <TabBar ariaLabel="Workspace tabs" items={items} activeKey={active} onChange={setActive} />
      </StoryFrame>;
  }
}`,...(s=(r=e.parameters)==null?void 0:r.docs)==null?void 0:s.source}}};const y=["Default"];export{e as Default,y as __namedExportsOrder,v as default};
