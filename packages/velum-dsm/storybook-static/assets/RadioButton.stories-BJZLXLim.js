import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{r as s}from"./index-hZsgmmNh.js";import{f as n}from"./VelumProvider-Cnx-m3OC.js";import{S as u}from"./_helpers-N5hE6fGh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const g={title:"Components/RadioButton",component:n},t={render:()=>{const[r,o]=s.useState("dry_run");return e.jsx(u,{children:e.jsxs("div",{style:{display:"grid",gap:"12px"},children:[e.jsx(n,{name:"mode",label:"Dry Run",description:"Preview the outbound payload without sending it.",checked:r==="dry_run",onChange:()=>o("dry_run")}),e.jsx(n,{name:"mode",label:"Live Execute",description:"Send changes to the integration target.",checked:r==="live",onChange:()=>o("live")})]})})}};var a,i,d;t.parameters={...t.parameters,docs:{...(a=t.parameters)==null?void 0:a.docs,source:{originalSource:`{
  render: () => {
    const [value, setValue] = useState("dry_run");
    return <StoryFrame>
        <div style={{
        display: "grid",
        gap: "12px"
      }}>
          <RadioButton name="mode" label="Dry Run" description="Preview the outbound payload without sending it." checked={value === "dry_run"} onChange={() => setValue("dry_run")} />
          <RadioButton name="mode" label="Live Execute" description="Send changes to the integration target." checked={value === "live"} onChange={() => setValue("live")} />
        </div>
      </StoryFrame>;
  }
}`,...(d=(i=t.parameters)==null?void 0:i.docs)==null?void 0:d.source}}};const y=["Default"];export{t as Default,y as __namedExportsOrder,g as default};
