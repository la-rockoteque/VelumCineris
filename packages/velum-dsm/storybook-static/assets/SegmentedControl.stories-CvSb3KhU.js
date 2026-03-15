import{n as o,f as u,j as r}from"./iframe-v_xVpIIQ.js";import{S as i}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const p={title:"Components/SegmentedControl",component:o,args:{value:"",options:[],onChange:()=>{},ariaLabel:"Choices"}},e={render:()=>{const[s,l]=u.useState("dry_run");return r.jsx(i,{children:r.jsx(o,{ariaLabel:"Mode",value:s,onChange:l,options:[{value:"dry_run",label:"Dry Run"},{value:"live",label:"Live Execute"}]})})}};var a,n,t;e.parameters={...e.parameters,docs:{...(a=e.parameters)==null?void 0:a.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("dry_run");
    return <StoryFrame>
        <SegmentedControl ariaLabel="Mode" value={value} onChange={setValue} options={[{
        value: "dry_run",
        label: "Dry Run"
      }, {
        value: "live",
        label: "Live Execute"
      }]} />
      </StoryFrame>;
  }
}`,...(t=(n=e.parameters)==null?void 0:n.docs)==null?void 0:t.source}}};const v=["Default"];export{e as Default,v as __namedExportsOrder,p as default};
