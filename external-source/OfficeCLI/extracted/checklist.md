# OfficeCLI Extraction Checklist

## Before Reading

- [x] Import upstream source into `external-source/OfficeCLI/`
- [x] Record official repository and imported commit
- [x] Detect license file
- [ ] Run deeper copyright and notice review if deriving a playbook or skill

## Reading

- [ ] Read upstream `README.md`
- [ ] Read upstream `SKILL.md`
- [ ] Review command model and examples
- [ ] Review schemas and plugin protocol
- [ ] Review install and binary distribution flow

## Extraction

- [ ] Identify reusable workflow patterns
- [ ] Separate upstream-specific details from project-local rules
- [ ] Draft project-local summary
- [ ] Draft candidate playbook or checklist if useful
- [ ] Add source attribution to any derived artifact

## Validation

- [ ] Verify command examples against current OfficeCLI release before recommending live usage
- [ ] Confirm install steps in the relevant OS environment
- [ ] Avoid copying upstream examples or long text into derived artifacts without license review
