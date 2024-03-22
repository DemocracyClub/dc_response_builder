# DCResponseBuilder
Data models and response builder for various DC projects


## Why does this project exist?

DC has a few different projects each with complex domain models.

Each project feeds in to other projects in various ways, and some of them
have public facing API endpoints.

We need two things:

1. To verify that fixture data in all our projects are using the right structures. In other words, if we have test fixtures as lumps of JSON in each project, how do we know that the schema is correct?
2. To provide a set of example cases that help us write better tests. Due to the complex nature of the domain, some tests are hard to create and we can't just use live service data. Consider that the number of elections on a given day can change a lot (from 0 to 4 or more). The number of dates in the future with elections can change, and for each ballot there is a huge matrix of edge cases. 

By providing a schema validator and tooling for creating fixtures both problems can be improved.

## Design principles


The users of this library are developers working on DC projects. Typically, this will be
in a test of some sort.

Because of this, it should be really obvious what data is being used. 

The project uses [the builder pattern](https://refactoring.guru/design-patterns/builder) to be explicit both about what's being added to each model, and to allow for maximum flexibility.

Broadly speaking the builders should make it hard to create really broken responses.

For example, if a ballot is cancelled we can sometimes add a cancellation reason. If we call `ballot.with_cancellation_reason(...)` that method should also set `cancelled=True` on the ballot.

If the test wants `cancelled=False` when there's a cancellation reason (for example to check if that causes problems in the project), it can always set the field to cancelled directly.
