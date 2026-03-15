import{j as e,C as d,i as o}from"./iframe-v_xVpIIQ.js";import"./preload-helper-Dp1pzeXC.js";const l={title:"Assets/Icons"},r={render:()=>e.jsx(d,{title:"Icons",subtitle:"DSM icon asset set rendered as a reference grid.",children:e.jsx("div",{style:{display:"grid",gridTemplateColumns:"repeat(auto-fit, minmax(140px, 1fr))",gap:"16px"},children:Object.entries(o).map(([t,a])=>e.jsxs("div",{style:{display:"grid",gap:"10px",padding:"16px",borderRadius:"12px",border:"1px solid var(--border)",background:"var(--surface-strong)",justifyItems:"center"},children:[e.jsx("img",{src:a,alt:t,style:{width:"56px",height:"56px",objectFit:"contain"}}),e.jsx("div",{style:{fontWeight:700},children:t})]},t))})})};var s,n,i;r.parameters={...r.parameters,docs:{...(s=r.parameters)==null?void 0:s.docs,source:{originalSource:`{
  render: () => <Card title="Icons" subtitle="DSM icon asset set rendered as a reference grid.">
      <div style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
      gap: "16px"
    }}>
        {Object.entries(iconAssets).map(([name, url]) => <div key={name} style={{
        display: "grid",
        gap: "10px",
        padding: "16px",
        borderRadius: "12px",
        border: "1px solid var(--border)",
        background: "var(--surface-strong)",
        justifyItems: "center"
      }}>
            <img src={url} alt={name} style={{
          width: "56px",
          height: "56px",
          objectFit: "contain"
        }} />
            <div style={{
          fontWeight: 700
        }}>{name}</div>
          </div>)}
      </div>
    </Card>
}`,...(i=(n=r.parameters)==null?void 0:n.docs)==null?void 0:i.source}}};const x=["Default"];export{r as Default,x as __namedExportsOrder,l as default};
