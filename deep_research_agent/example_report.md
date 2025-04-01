# Why pgvector is Not Part of Core PostgreSQL: An Analysis

## Understanding pgvector: Functionality and Purpose

pgvector is an open-source PostgreSQL extension that provides vector similarity search capabilities. It introduces a dedicated data type, operators, and functions for efficient storage and manipulation of high-dimensional vector data. This extension enables important functionality for modern applications:

- Vector similarity searches based on metrics like cosine similarity and Euclidean distance
- Support for applications such as semantic search, recommendation systems, and natural language processing
- Storage of vectors directly in PostgreSQL tables, facilitating efficient retrieval and analysis
- Integration with PostgreSQL's existing features such as transaction management and query optimization

The latest version of pgvector (v0.5.0) adds a new index type and improves performance for distance operations, showing ongoing development and improvement of this extension.

## PostgreSQL's Extension Philosophy

While my research didn't uncover explicit statements from PostgreSQL developers about their philosophy regarding core vs. extensions, we can infer the likely rationale based on observed patterns and general database design principles:

1. **Modular Design**: PostgreSQL follows a modular architecture that allows specialized functionality to be added through extensions without bloating the core database. This keeps the core database lean and focused on general-purpose functionality.

2. **Specialized vs. General-Purpose Functionality**: Core PostgreSQL tends to include features that are broadly useful across many use cases, while more specialized functionality is often implemented as extensions. Vector similarity search, while increasingly important, is still a specialized use case that isn't needed by all PostgreSQL users.

3. **Maintenance and Development Velocity**: Extensions can evolve at their own pace, allowing for more rapid development and experimentation compared to core features that must maintain strict backward compatibility and undergo more rigorous review processes.

4. **Optional Installation**: Extensions allow users to install only the functionality they need, reducing resource usage and potential attack surface for those who don't require certain features.

## Technical Considerations for pgvector as an Extension

There are several technical factors that likely contribute to pgvector being maintained as an extension rather than integrated into core PostgreSQL:

1. **Performance Characteristics**: pgvector has specific performance characteristics and limitations that differ from typical relational database operations. As noted in my research, pgvector has scalability issues with high-dimensional vectors and only supports one type of index called IVFFlat, limiting its performance and capabilities compared to dedicated vector databases.

2. **Specialized Use Case**: Vector similarity search is a specialized functionality primarily used for AI and machine learning applications, not a fundamental database operation needed by most users.

3. **Ongoing Development**: Vector search technology is rapidly evolving, and keeping pgvector as an extension allows it to evolve quickly without being constrained by PostgreSQL's release cycle.

4. **Resource Requirements**: Vector operations can be computationally intensive and memory-hungry. Keeping this functionality as an optional extension allows users who don't need vector capabilities to avoid the associated overhead.

  0
## Comparison with Other PostgreSQL Extensions

pgvector follows a pattern seen with other specialized PostgreSQL extensions that provide important but not universally needed functionality:

1. **pgcrypto**: Despite the importance of cryptographic functions, pgcrypto remains an extension rather than core functionality. Like vector search, cryptographic operations are not needed by all database users and benefit from being optional.

2. **PostGIS**: Spatial data handling is another example of specialized functionality that remains an extension despite its widespread use in certain domains. Like pgvector, PostGIS provides functionality that is critical for some applications but unnecessary for many others.

These examples suggest that PostgreSQL has a consistent approach to keeping specialized functionality as extensions, even when that functionality is widely used in certain domains or applications.

## Benefits of pgvector as an Extension

Maintaining pgvector as an extension rather than integrating it into core PostgreSQL offers several benefits:

1. **Flexibility for Users**: Users can choose whether to install and enable pgvector based on their specific needs, avoiding unnecessary complexity and resource usage.

2. **Development Agility**: The pgvector development team can iterate quickly and release updates independently of PostgreSQL's release cycle.

3. **Specialized Optimization**: As an extension, pgvector can focus on optimizing specifically for vector operations without compromising PostgreSQL's general-purpose performance.

4. **Integration with PostgreSQL Ecosystem**: Despite being an extension, pgvector integrates seamlessly with PostgreSQL features such as transaction management and query optimization, offering the best of both worlds.

# Conclusion

The decision to maintain pgvector as an extension rather than integrating it into core PostgreSQL aligns with PostgreSQL's general philosophy of keeping specialized functionality separate from the core database. This approach allows the core database to remain lean and focused on general-purpose functionality while enabling specialized features to be added as needed through the extension system.

While vector similarity search is increasingly important for modern applications, particularly those involving AI and machine learning, its specialized nature and specific performance characteristics make it well-suited to implementation as an extension. This allows pgvector to evolve rapidly, optimizes resource usage for users who don't need vector capabilities, and maintains PostgreSQL's focus on being a robust, general-purpose relational database.

The pattern observed with pgvector is consistent with other specialized extensions like pgcrypto and PostGIS, suggesting that PostgreSQL has a deliberate strategy of implementing specialized functionality as extensions even when that functionality is widely used in certain domains. This modular approach has served PostgreSQL well, contributing to its reputation as a highly extensible and adaptable database system that can be tailored to a wide range of use cases.# Citations

- https://www.postgresql.org/about/news/pgvector-050-released-2700/
- https://www.timescale.com/learn/postgresql-extensions-pgvector
- https://medium.com/@zilliz_learn/getting-started-with-pgvector-a-guide-for-developers-exploring-vector-databases-9c2295bb13e5
- https://www.postgresql.org/docs/current/pgcrypto.html
