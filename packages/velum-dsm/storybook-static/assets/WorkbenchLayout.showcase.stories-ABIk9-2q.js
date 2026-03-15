import{j as e,O as d,Q as c,U as n,V as r,X as l,b as t,M as h,Y as m,L as u}from"./iframe-v_xVpIIQ.js";import{S as x,a as p,b as S}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const k={title:"Components/Workspace/WorkbenchLayout"},a={render:()=>e.jsx(x,{maxWidth:"1100px",children:e.jsx(p,{columns:"1fr",gap:"20px",children:e.jsx(S,{label:"Balanced Layout",description:"Standard sidebar + result surface",minHeight:"380px",children:e.jsxs(d,{children:[e.jsxs(c,{children:[e.jsxs(n,{children:[e.jsx(r,{children:"Controls"}),e.jsx(l,{children:"Sidebar area for filters, forms, and quick actions."}),e.jsx(t,{$variant:"primary",children:"Run"}),e.jsx(t,{children:"Reload"})]}),e.jsxs(n,{children:[e.jsx(r,{children:"Summary"}),e.jsx(h,{children:"2 pending changes"})]})]}),e.jsx(m,{children:e.jsxs(n,{children:[e.jsx(r,{children:"Results"}),e.jsx(u,{children:`romanized: ashmar
symbolized: ASH-MR`})]})})]})})})})};var s,i,o;a.parameters={...a.parameters,docs:{...(s=a.parameters)==null?void 0:s.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1100px">
      <StateMatrix columns="1fr" gap="20px">
        <StateCase label="Balanced Layout" description="Standard sidebar + result surface" minHeight="380px">
          <WorkbenchLayout>
            <WorkbenchSidebar>
              <InsetCard>
                <InsetTitle>Controls</InsetTitle>
                <InsetLead>Sidebar area for filters, forms, and quick actions.</InsetLead>
                <Button $variant="primary">Run</Button>
                <Button>Reload</Button>
              </InsetCard>
              <InsetCard>
                <InsetTitle>Summary</InsetTitle>
                <MetaText>2 pending changes</MetaText>
              </InsetCard>
            </WorkbenchSidebar>
            <WorkbenchMain>
              <InsetCard>
                <InsetTitle>Results</InsetTitle>
                <WorkspaceOutput>{\`romanized: ashmar\\nsymbolized: ASH-MR\`}</WorkspaceOutput>
              </InsetCard>
            </WorkbenchMain>
          </WorkbenchLayout>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(o=(i=a.parameters)==null?void 0:i.docs)==null?void 0:o.source}}};const W=["Showcase"];export{a as Showcase,W as __namedExportsOrder,k as default};
