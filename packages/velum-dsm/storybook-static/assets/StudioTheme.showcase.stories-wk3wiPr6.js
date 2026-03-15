import{j as e}from"./jsx-runtime-Bll8AAhy.js";import{C as p,B as t,b as n,n as l,Q as m}from"./VelumProvider-Cnx-m3OC.js";import{S as c,a as x,b as h}from"./_helpers-N5hE6fGh.js";import"./index-hZsgmmNh.js";import"./_commonjsHelpers-gnU0ypJ3.js";const j={title:"Tokens/StudioTheme"},a={render:()=>e.jsx(c,{maxWidth:"980px",children:e.jsx(x,{children:e.jsx(h,{label:"Surface Composition",description:"Theme tokens applied as a composed fragment",minHeight:"260px",children:e.jsx(p,{title:"Studio Theme Showcase",subtitle:"Theme tokens applied as a composed interface fragment.",children:e.jsxs("div",{style:{display:"grid",gap:"16px"},children:[e.jsxs("div",{style:{display:"flex",gap:"12px",flexWrap:"wrap"},children:[e.jsx(t,{tone:"ok",children:"Healthy"}),e.jsx(t,{tone:"warn",children:"Pending"}),e.jsx(t,{tone:"danger",children:"Blocked"})]}),e.jsxs("div",{style:{display:"flex",gap:"12px",flexWrap:"wrap"},children:[e.jsx(n,{$variant:"primary",children:"Primary"}),e.jsx(n,{children:"Secondary"}),e.jsx(n,{$variant:"ghost",children:"Ghost"})]}),e.jsx(l,{children:Object.entries(m).map(([o,d])=>`${o}: ${d}`).slice(0,4).join(" · ")})]})})})})})};var r,s,i;a.parameters={...a.parameters,docs:{...(r=a.parameters)==null?void 0:r.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Surface Composition" description="Theme tokens applied as a composed fragment" minHeight="260px">
          <Card title="Studio Theme Showcase" subtitle="Theme tokens applied as a composed interface fragment.">
            <div style={{
            display: "grid",
            gap: "16px"
          }}>
              <div style={{
              display: "flex",
              gap: "12px",
              flexWrap: "wrap"
            }}>
                <Badge tone="ok">Healthy</Badge>
                <Badge tone="warn">Pending</Badge>
                <Badge tone="danger">Blocked</Badge>
              </div>
              <div style={{
              display: "flex",
              gap: "12px",
              flexWrap: "wrap"
            }}>
                <Button $variant="primary">Primary</Button>
                <Button>Secondary</Button>
                <Button $variant="ghost">Ghost</Button>
              </div>
              <MetaText>{Object.entries(studioTheme).map(([key, value]) => \`\${key}: \${value}\`).slice(0, 4).join(" · ")}</MetaText>
            </div>
          </Card>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(i=(s=a.parameters)==null?void 0:s.docs)==null?void 0:i.source}}};const B=["Showcase"];export{a as Showcase,B as __namedExportsOrder,j as default};
