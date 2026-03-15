import{j as e,P as o}from"./iframe-v_xVpIIQ.js";import{S as s,a as c,b as r,D as a}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const h={title:"Components/Layout/PanelGrid"},n={render:()=>e.jsx(s,{maxWidth:"1100px",children:e.jsxs(c,{children:[e.jsx(r,{label:"Four Panels",description:"Balanced grid with equal cards",minHeight:"260px",children:e.jsxs(o,{$min:"200px",children:[e.jsx(a,{children:"Panel 1"}),e.jsx(a,{children:"Panel 2"}),e.jsx(a,{children:"Panel 3"}),e.jsx(a,{children:"Panel 4"})]})}),e.jsx(r,{label:"Narrow Min Width",description:"More aggressive auto-fit layout",minHeight:"260px",children:e.jsxs(o,{$min:"140px",children:[e.jsx(a,{children:"A"}),e.jsx(a,{children:"B"}),e.jsx(a,{children:"C"}),e.jsx(a,{children:"D"}),e.jsx(a,{children:"E"})]})})]})})};var l,i,t;n.parameters={...n.parameters,docs:{...(l=n.parameters)==null?void 0:l.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="1100px">
      <StateMatrix>
        <StateCase label="Four Panels" description="Balanced grid with equal cards" minHeight="260px">
          <PanelGrid $min="200px">
            <DemoBlock>Panel 1</DemoBlock>
            <DemoBlock>Panel 2</DemoBlock>
            <DemoBlock>Panel 3</DemoBlock>
            <DemoBlock>Panel 4</DemoBlock>
          </PanelGrid>
        </StateCase>
        <StateCase label="Narrow Min Width" description="More aggressive auto-fit layout" minHeight="260px">
          <PanelGrid $min="140px">
            <DemoBlock>A</DemoBlock>
            <DemoBlock>B</DemoBlock>
            <DemoBlock>C</DemoBlock>
            <DemoBlock>D</DemoBlock>
            <DemoBlock>E</DemoBlock>
          </PanelGrid>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(t=(i=n.parameters)==null?void 0:i.docs)==null?void 0:t.source}}};const p=["Showcase"];export{n as Showcase,p as __namedExportsOrder,h as default};
