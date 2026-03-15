import{o,f as m,j as a}from"./iframe-v_xVpIIQ.js";import{S as c}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const b={title:"Components/TabBar",component:o,args:{items:[],activeKey:"",onChange:()=>{},ariaLabel:"Tabs"}},l=[{key:"compendium",label:"Compendium"},{key:"details",label:"Details"},{key:"translator",label:"Translator"},{key:"image",label:"Image"}],e={render:()=>{const[n,i]=m.useState("compendium");return a.jsx(c,{maxWidth:"980px",children:a.jsx(o,{ariaLabel:"Sheet selector",items:l,activeKey:n,onChange:i})})}};var t,r,s;e.parameters={...e.parameters,docs:{...(t=e.parameters)==null?void 0:t.docs,source:{originalSource:`{
  render: () => {
    const [active, setActive] = useState("compendium");
    return <StoryFrame maxWidth="980px">
        <TabBar ariaLabel="Sheet selector" items={items} activeKey={active} onChange={setActive} />
      </StoryFrame>;
  }
}`,...(s=(r=e.parameters)==null?void 0:r.docs)==null?void 0:s.source}}};const x=["Default"];export{e as Default,x as __namedExportsOrder,b as default};
