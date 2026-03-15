import{j as t,A as a,b as e}from"./iframe-v_xVpIIQ.js";import{S as l,a as c,b as r}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const u={title:"Components/Actions/ActionRow"},n={render:()=>t.jsx(l,{children:t.jsxs(c,{children:[t.jsx(r,{label:"Standard",description:"Common multi-action row",children:t.jsxs(a,{children:[t.jsx(e,{$variant:"primary",children:"Save"}),t.jsx(e,{children:"Reload"}),t.jsx(e,{children:"Validate"}),t.jsx(e,{$variant:"ghost",children:"Reset"})]})}),t.jsx(r,{label:"Wrapping",description:"Long labels still wrap cleanly",minHeight:"96px",children:t.jsxs(a,{children:[t.jsx(e,{$variant:"primary",children:"Publish to Google Docs"}),t.jsx(e,{children:"Generate Homebrewery Preview"})]})})]})})};var o,i,s;n.parameters={...n.parameters,docs:{...(o=n.parameters)==null?void 0:o.docs,source:{originalSource:`{
  render: () => <StoryFrame>
      <StateMatrix>
        <StateCase label="Standard" description="Common multi-action row">
          <ActionRow>
            <Button $variant="primary">Save</Button>
            <Button>Reload</Button>
            <Button>Validate</Button>
            <Button $variant="ghost">Reset</Button>
          </ActionRow>
        </StateCase>
        <StateCase label="Wrapping" description="Long labels still wrap cleanly" minHeight="96px">
          <ActionRow>
            <Button $variant="primary">Publish to Google Docs</Button>
            <Button>Generate Homebrewery Preview</Button>
          </ActionRow>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(s=(i=n.parameters)==null?void 0:i.docs)==null?void 0:s.source}}};const x=["Showcase"];export{n as Showcase,x as __namedExportsOrder,u as default};
