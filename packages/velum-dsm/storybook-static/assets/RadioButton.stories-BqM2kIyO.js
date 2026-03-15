import{h as n,f as i,j as e}from"./iframe-v_xVpIIQ.js";import{S as u}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const p={title:"Components/RadioButton",component:n},t={render:()=>{const[r,a]=i.useState("dry_run");return e.jsx(u,{children:e.jsxs("div",{style:{display:"grid",gap:"12px"},children:[e.jsx(n,{name:"mode",label:"Dry Run",description:"Preview the outbound payload without sending it.",checked:r==="dry_run",onChange:()=>a("dry_run")}),e.jsx(n,{name:"mode",label:"Live Execute",description:"Send changes to the integration target.",checked:r==="live",onChange:()=>a("live")})]})})}};var o,d,s;t.parameters={...t.parameters,docs:{...(o=t.parameters)==null?void 0:o.docs,source:{originalSource:`{
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
}`,...(s=(d=t.parameters)==null?void 0:d.docs)==null?void 0:s.source}}};const h=["Default"];export{t as Default,h as __namedExportsOrder,p as default};
