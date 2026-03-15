import{j as e,f as u,n as p}from"./iframe-v_xVpIIQ.js";import{S as m,a as x,b as t}from"./_helpers-j3YeHUq4.js";import"./preload-helper-Dp1pzeXC.js";const b={title:"Components/SegmentedControl"};function i(n){const[o,c]=u.useState(n.initialValue);return e.jsx(p,{ariaLabel:"Example choices",value:o,onChange:c,options:n.options})}const a={render:()=>e.jsx(m,{maxWidth:"980px",children:e.jsxs(x,{children:[e.jsx(t,{label:"Binary Choice",description:"Short high-signal decision set",minHeight:"120px",children:e.jsx(i,{initialValue:"dry_run",options:[{value:"dry_run",label:"Dry Run"},{value:"live",label:"Live Execute"}]})}),e.jsx(t,{label:"Three Options",description:"Small enum picker",minHeight:"120px",children:e.jsx(i,{initialValue:"balance",options:[{value:"balance",label:"Balance"},{value:"rewrite",label:"Rewrite"},{value:"qa",label:"QA"}]})})]})})};var l,r,s;a.parameters={...a.parameters,docs:{...(l=a.parameters)==null?void 0:l.docs,source:{originalSource:`{
  render: () => <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Binary Choice" description="Short high-signal decision set" minHeight="120px">
          <Example initialValue="dry_run" options={[{
          value: "dry_run",
          label: "Dry Run"
        }, {
          value: "live",
          label: "Live Execute"
        }]} />
        </StateCase>
        <StateCase label="Three Options" description="Small enum picker" minHeight="120px">
          <Example initialValue="balance" options={[{
          value: "balance",
          label: "Balance"
        }, {
          value: "rewrite",
          label: "Rewrite"
        }, {
          value: "qa",
          label: "QA"
        }]} />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
}`,...(s=(r=a.parameters)==null?void 0:r.docs)==null?void 0:s.source}}};const v=["Showcase"];export{a as Showcase,v as __namedExportsOrder,b as default};
